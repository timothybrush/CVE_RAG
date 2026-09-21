# Readable CVE records

Grouped by the year in each CVE ID, not its publication date. The **September 21, 2026 incremental update adds 6,486 newly published CVEs**, with publication dates after **2026-09-09T14:42:39Z** through **2026-09-21T21:13:12Z**. Existing records and the rejected file are unchanged.

This is a mixed snapshot. Existing records from 1999–2025 retain the July 13 snapshot, and existing 2026 records retain the September 9 refresh. New publications can have older CVE ID years and are added to the corresponding year file. Per-record source dates and the manifest distinguish those cohorts.

New records use CVE commit `88dff49c694d47699a7e29ff2d15ab5915ff27bd`, NVD feeds plus API updates through the new cutoff, EPSS scores from `2026-09-21T12:03:23Z`, and KEV catalog `2026.09.21`. Weekly updates append newly published records only; existing records are not refreshed or revalidated against current source statuses.

These are the canonical, indented JSON arrays of `id`, `text`, and `metadata` record objects. IDs are unique and sorted numerically. The uploader reads these same files and excludes `rejected.json`. [`manifest.json`](manifest.json) records file counts/checksums, original snapshot provenance, each publication window, and the next incremental cutoff.

Records are bounded summaries; `text_truncated` and `*_overflow_count` identify omissions, with source links for the complete record. Missing optional enrichment means unavailable or unassessed. Solution/workaround guidance does not prove a working fix exists. New NVD product labels retain their conditional applicability scope.

Run `python upload_to_pinecone.py --dry-run` from the repository root to validate the corpus without API calls. See the [main README](../README.md) for Git LFS and upload instructions.

| File | Records | Newly added |
| --- | ---: | ---: |
| [CVE-1999.json](CVE-1999.json) | 1,540 | 0 |
| [CVE-2000.json](CVE-2000.json) | 1,236 | 0 |
| [CVE-2001.json](CVE-2001.json) | 1,537 | 0 |
| [CVE-2002.json](CVE-2002.json) | 2,357 | 0 |
| [CVE-2003.json](CVE-2003.json) | 1,504 | 0 |
| [CVE-2004.json](CVE-2004.json) | 2,644 | 0 |
| [CVE-2005.json](CVE-2005.json) | 4,627 | 0 |
| [CVE-2006.json](CVE-2006.json) | 6,995 | 0 |
| [CVE-2007.json](CVE-2007.json) | 6,458 | 0 |
| [CVE-2008.json](CVE-2008.json) | 7,005 | 0 |
| [CVE-2009.json](CVE-2009.json) | 4,921 | 0 |
| [CVE-2010.json](CVE-2010.json) | 5,074 | 0 |
| [CVE-2011.json](CVE-2011.json) | 4,646 | 0 |
| [CVE-2012.json](CVE-2012.json) | 5,488 | 0 |
| [CVE-2013.json](CVE-2013.json) | 6,221 | 0 |
| [CVE-2014.json](CVE-2014.json) | 8,427 | 0 |
| [CVE-2015.json](CVE-2015.json) | 8,111 | 0 |
| [CVE-2016.json](CVE-2016.json) | 9,365 | 0 |
| [CVE-2017.json](CVE-2017.json) | 14,761 | 1 |
| [CVE-2018.json](CVE-2018.json) | 16,188 | 0 |
| [CVE-2019.json](CVE-2019.json) | 16,094 | 1 |
| [CVE-2020.json](CVE-2020.json) | 19,387 | 1 |
| [CVE-2021.json](CVE-2021.json) | 22,588 | 2 |
| [CVE-2022.json](CVE-2022.json) | 26,427 | 2 |
| [CVE-2023.json](CVE-2023.json) | 30,630 | 33 |
| [CVE-2024.json](CVE-2024.json) | 38,399 | 11 |
| [CVE-2025.json](CVE-2025.json) | 43,224 | 48 |
| [CVE-2026.json](CVE-2026.json) | 61,249 | 6,387 |
| [rejected.json](rejected.json) | 868 | 0 |

**Total:** 377,103 searchable records plus 868 rejected records kept separately.
