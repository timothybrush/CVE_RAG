#!/usr/bin/env python3
"""Create or verify the serverless Pinecone index used by this corpus."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_env(path: Path) -> None:
    """Load the small KEY=VALUE .env format used by this repository."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if value[:1] == value[-1:] and value[:1] in {"'", '"'}:
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def parser() -> argparse.ArgumentParser:
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--env-file", type=Path, default=ROOT / ".env")
    known, _ = pre.parse_known_args()
    load_env(known.env_file.expanduser())

    p = argparse.ArgumentParser(
        parents=[pre],
        description="Create a cosine Pinecone serverless index, or verify an existing one.",
    )
    p.add_argument(
        "--index",
        default=os.getenv("PINECONE_INDEX_NAME", "cve-rag"),
        help="index name (default: PINECONE_INDEX_NAME or cve-rag)",
    )
    p.add_argument(
        "--dimension",
        type=positive_int,
        default=positive_int(os.getenv("OPENAI_EMBED_DIMENSION", "1536")),
        help="embedding dimension (default: OPENAI_EMBED_DIMENSION or 1536)",
    )
    p.add_argument("--cloud", default=os.getenv("PINECONE_CLOUD", "aws"))
    p.add_argument("--region", default=os.getenv("PINECONE_REGION", "us-east-1"))
    p.add_argument("--timeout", type=positive_int, default=300, help="creation timeout in seconds")
    p.add_argument("--dry-run", action="store_true", help="print the requested index without using Pinecone")
    return p


def field(value: object, name: str) -> object | None:
    if isinstance(value, dict):
        return value.get(name)
    return getattr(value, name, None)


def verify_index(current: object, args: argparse.Namespace) -> None:
    """Require the complete contract this uploader depends on."""
    dimension = field(current, "dimension")
    metric = field(current, "metric")
    vector_type = field(current, "vector_type")
    integrated_embed = field(current, "embed")
    status = field(current, "status")
    ready = field(status, "ready") if status is not None else None
    spec = field(current, "spec")
    serverless = field(spec, "serverless") if spec is not None else None
    deployment = serverless if serverless is not None else spec
    cloud = field(deployment, "cloud") if deployment is not None else None
    region = field(deployment, "region") if deployment is not None else None

    errors: list[str] = []
    if dimension != args.dimension:
        errors.append(f"dimension={dimension!r}")
    if metric != "cosine":
        errors.append(f"metric={metric!r}")
    if vector_type not in {None, "dense"}:
        errors.append(f"vector_type={vector_type!r}")
    if integrated_embed is not None:
        errors.append("integrated_embedding=enabled")
    if ready is not True:
        errors.append(f"ready={ready!r}")
    if cloud != args.cloud or region != args.region:
        errors.append(f"serverless={cloud!r}/{region!r}")
    if errors:
        raise SystemExit(
            "error: existing index does not match the requested ready dense serverless contract: "
            + ", ".join(errors)
        )


def main() -> int:
    args = parser().parse_args()
    if not args.index.strip():
        raise SystemExit("error: index name cannot be empty")

    requested = (
        f"index={args.index} dimension={args.dimension} metric=cosine "
        f"serverless={args.cloud}/{args.region}"
    )
    if args.dry_run:
        print(f"Dry run: would create or verify {requested}")
        return 0

    api_key = os.getenv("PINECONE_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("error: set PINECONE_API_KEY in .env or the environment")
    try:
        from pinecone import Pinecone, ServerlessSpec
    except ImportError as exc:
        raise SystemExit("error: install dependencies with: pip install -r requirements.txt") from exc

    pc = Pinecone(api_key=api_key)
    if pc.indexes.exists(args.index):
        current = pc.indexes.describe(args.index)
        verify_index(current, args)
        print(f"Ready: existing {requested}")
        return 0

    pc.indexes.create(
        name=args.index,
        dimension=args.dimension,
        metric="cosine",
        spec=ServerlessSpec(cloud=args.cloud, region=args.region),
        timeout=args.timeout,
    )
    current = pc.indexes.describe(args.index)
    verify_index(current, args)
    print(f"Created: {requested}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)
