"""Offline regression checks for the paid bulk-import path; all HTTP is mocked."""

import json
import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import httpx
import orjson
from pinecone import Index
from pinecone.errors import ApiError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import upload_to_pinecone as uploader


def record(number, text="Offline classroom evidence.", state="PUBLISHED"):
    return {
        "id": f"CVE-2026-{number:04d}",
        "text": text,
        "metadata": {"state": state, "vendors": ["fixture"]},
    }


class BatchTests(unittest.TestCase):
    def test_wire_bytes_include_float_encoding_and_namespace(self):
        vectors = [
            {"id": str(i), "values": [.01234566979110241, -.00001] * 768,
             "metadata": {"text": "Fixture 😀", "cvss": 9.8}}
            for i in range(100)
        ]
        for namespace in ("", 'class-😀-"-\\'):
            with self.subTest(namespace=namespace):
                batches = list(uploader.vector_batches(vectors, 1_800_000, namespace))
                self.assertGreater(len(batches), 1)
                self.assertEqual(sum(map(len, batches)), 100)
                for batch in batches:
                    body = {"vectors": batch}
                    if namespace:
                        body["namespace"] = namespace
                    self.assertLessEqual(len(orjson.dumps(body)), 1_800_000)

    def test_vector_count_and_exact_size_boundaries(self):
        vectors = [{"id": str(i), "values": [0.0], "metadata": {}} for i in range(1005)]
        self.assertEqual([len(x) for x in uploader.vector_batches(vectors, 2_000_000)], [1000, 5])
        single = [{"id": "only", "values": [1.0], "metadata": {"text": "x" * 500}}]
        size = len(orjson.dumps({"vectors": single, "namespace": "course"}))
        self.assertEqual(list(uploader.vector_batches(single, size, "course")), [single])
        with self.assertRaises(ValueError):
            list(uploader.vector_batches(single, size - 1, "course"))

    def test_embedding_budgets_and_settings(self):
        records = [record(1000 + i, "x" * 8192) for i in range(40)]
        batches = list(uploader.embedding_batches(records, 100))
        self.assertEqual([len(x) for x in batches], [36, 4])
        for batch in batches:
            self.assertLessEqual(sum(len(r["text"].encode()) for r in batch), 300_000)
        with self.assertRaises(ValueError):
            list(uploader.embedding_batches([record(1000, "x" * 8193)], 100))
        with self.assertRaises(ValueError):
            list(uploader.embedding_batches([record(1000)], 2049))
        with self.assertRaises(ValueError):
            uploader.validate_record(record(1000, "x" * 8193), "fixture", searchable=True)
        for model, dimension in [("text-embedding-3-small", 1537), ("text-embedding-ada-002", 1536)]:
            with self.subTest(model=model), self.assertRaises(ValueError):
                uploader.validate_embedding_settings(model, dimension)

    def test_malformed_embedding_indices_and_oversized_request(self):
        client = SimpleNamespace(embeddings=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(
            data=[SimpleNamespace(index=0, embedding=[.1, .2]),
                  SimpleNamespace(index=0, embedding=[.3, .4])]
        )))
        args = SimpleNamespace(model="text-embedding-3-small", dimension=2, retries=1)
        with self.assertRaises(RuntimeError):
            uploader.embed_batch(client, [record(1000), record(1001)], args)
        with self.assertRaises(ValueError):
            uploader.embed_batch(client, [record(i, "x" * 8192) for i in range(40)], args)

    def test_permanent_rejection_stops_and_throttling_retries(self):
        with patch.object(uploader.time, "sleep"):
            operation = unittest.mock.Mock(side_effect=ApiError("fixture rejection", 400))
            with self.assertRaises(RuntimeError):
                uploader.retry("fixture", operation, 5)
            self.assertEqual(operation.call_count, 1)
            operation = unittest.mock.Mock(side_effect=[ApiError("fixture throttle", 429), "ok"])
            self.assertEqual(uploader.retry("fixture", operation, 5), "ok")
            self.assertEqual(operation.call_count, 2)


class UploadTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cve-uploader-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "data").mkdir()
        self.records = [record(i) for i in range(1000, 1005)]
        entries = []
        for name, rows in [("CVE-2026.json", self.records),
                           ("rejected.json", [record(1999, state="REJECTED")])]:
            path = self.root / "data" / name
            path.write_text(json.dumps(rows), encoding="utf-8")
            entries.append({"path": f"data/{name}", "bytes": path.stat().st_size,
                            "record_count": len(rows), "sha256": uploader.sha256(path),
                            "first_id": rows[0]["id"], "last_id": rows[-1]["id"]})
        manifest = {"format": "portable-cve-rag", "schema_version": 2,
                    "storage_format": "json-array", "partitioning": "cve-id-year",
                    "counts": {"search": 5, "rejected": 1, "total": 6},
                    "search_files": [entries[0]], "rejected_file": entries[1]}
        path = self.root / "data" / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.dataset = uploader.validate_dataset(path)
        self.args = SimpleNamespace(index="offline", namespace="class-😀", model="text-embedding-3-small",
                                    dimension=16, batch_size=5, retries=1, upsert_max_bytes=1000,
                                    limit=None, checkpoint=self.root / "checkpoint.json")
        self.host = "https://offline.invalid"
        self.index = Index(host=self.host, api_key="offline-placeholder")
        self.addCleanup(self.index.close)
        self.stored = {}
        self.calls = 0
        self.fail_at = None
        self.bad_ack = False

    def post(self, path, **kwargs):
        if path == "/describe_index_stats":
            namespaces = {self.args.namespace: {"vectorCount": len(self.stored)}} if self.stored else {}
            return httpx.Response(200, json={"namespaces": namespaces, "dimension": 16,
                                            "totalVectorCount": len(self.stored)})
        self.assertEqual(path, "/vectors/upsert")
        body = kwargs["json"]
        self.assertLessEqual(len(orjson.dumps(body)), self.args.upsert_max_bytes)
        self.assertEqual(body["namespace"], self.args.namespace)
        self.calls += 1
        if self.calls == self.fail_at:
            raise ApiError("fixture outage", 503)
        for vector in body["vectors"]:
            self.stored[vector["id"]] = vector
        return httpx.Response(200, json={"upsertedCount": 0 if self.bad_ack else len(body["vectors"])})

    def get(self, path, **kwargs):
        self.assertEqual(path, "/vectors/fetch")
        wanted = kwargs["params"]["ids"]
        return httpx.Response(200, json={"vectors": {k: self.stored[k] for k in wanted if k in self.stored},
                                        "namespace": self.args.namespace})

    @contextmanager
    def offline_apis(self):
        harness = self

        class Pinecone:
            def __init__(self, **kwargs):
                self.indexes = SimpleNamespace(exists=lambda _: True, describe=lambda _: {
                    "dimension": 16, "metric": "cosine", "vector_type": "dense",
                    "host": harness.host, "status": {"ready": True}})

            def index(self, *, host):
                harness.assertEqual(host, harness.host)
                return harness.index

        class OpenAI:
            def __init__(self, **kwargs):
                self.embeddings = SimpleNamespace(create=lambda **kw: SimpleNamespace(data=[
                    SimpleNamespace(index=i, embedding=[.01234566979110241] * 16)
                    for i in range(len(kw["input"]))]))

        with patch.dict(os.environ, {"OPENAI_API_KEY": "offline-placeholder", "PINECONE_API_KEY": "offline-placeholder"}), \
             patch.dict(sys.modules, {"pinecone": SimpleNamespace(Pinecone=Pinecone), "openai": SimpleNamespace(OpenAI=OpenAI)}), \
             patch.object(self.index._http, "post", side_effect=self.post), \
             patch.object(self.index._http, "get", side_effect=self.get):
            yield

    def checkpoint(self):
        return uploader.read_checkpoint(self.args.checkpoint, uploader.checkpoint_contract(self.args, self.dataset))

    def test_interruption_resume_and_rejected_exclusion(self):
        self.assertNotIn("CVE-2026-1999", self.dataset.ids)
        with self.offline_apis():
            self.fail_at = 2
            with self.assertRaises(RuntimeError):
                uploader.upload(self.args, self.dataset, None, 0, None)
            checkpoint = self.checkpoint()
            self.assertGreater(checkpoint["uploaded"], 0)
            self.assertLess(checkpoint["uploaded"], 5)
            self.assertEqual(len(self.stored), checkpoint["uploaded"])
            self.fail_at = None
            self.assertEqual(uploader.upload(self.args, self.dataset, checkpoint["last_id"],
                                            checkpoint["uploaded"], checkpoint["index_host"]),
                             5 - checkpoint["uploaded"])
            checkpoint = self.checkpoint()
            self.assertEqual(checkpoint["uploaded"], 5)
            self.assertEqual(set(self.stored), {r["id"] for r in self.records})
            for item in self.records:
                self.assertEqual(self.stored[item["id"]]["metadata"]["text"], item["text"])
                self.assertEqual(self.stored[item["id"]]["metadata"]["cve_id"], item["id"])
            self.assertEqual(uploader.upload(self.args, self.dataset, checkpoint["last_id"], 5, self.host), 0)
            with self.assertRaises(ValueError):
                uploader.upload(self.args, self.dataset, checkpoint["last_id"], 5, "different.invalid")
            del self.stored[checkpoint["last_id"]]
            with self.assertRaises(ValueError):
                uploader.upload(self.args, self.dataset, checkpoint["last_id"], 5, self.host)

    def test_partial_acknowledgment_does_not_advance_checkpoint(self):
        self.bad_ack = True
        with self.offline_apis(), self.assertRaises(RuntimeError):
            uploader.upload(self.args, self.dataset, None, 0, None)
        self.assertFalse(self.args.checkpoint.exists())

    def test_occupied_namespace_requires_a_matching_resume(self):
        self.stored["old-snapshot-record"] = {}
        with self.offline_apis(), self.assertRaisesRegex(ValueError, "fresh --namespace"):
            uploader.upload(self.args, self.dataset, None, 0, None)
        self.assertEqual(self.calls, 0)
        self.assertFalse(self.args.checkpoint.exists())

    def test_unavailable_namespace_statistics_reject_upload(self):
        with self.offline_apis(), \
             patch.object(self.index, "describe_index_stats", return_value=SimpleNamespace(namespaces=None)), \
             self.assertRaisesRegex(ValueError, "could not verify"):
            uploader.upload(self.args, self.dataset, None, 0, None)
        self.assertEqual(self.calls, 0)


if __name__ == "__main__":
    unittest.main()
