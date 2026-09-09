# Readable CVE records

Grouped by the year in each CVE ID, not its publication date. Files for **1999–2025** retain the **2026-07-13** snapshot. The **2026** file uses CVE and NVD data checked through **2026-09-09T14:42:39Z**, September 9 EPSS scores, and CISA KEV catalog **2026.09.08**, released September 8.

These are the canonical corpus files. Each file is an indented JSON array of record objects with `id`, `text`, and `metadata` fields. The uploader reads these same files one year at a time and excludes `rejected.json`.

[`manifest.json`](manifest.json) records counts, byte sizes, SHA-256 checksums, exact source revisions, and per-source freshness. The 2026 CVE source is commit `4b39227ea1061a7bc8028b8e530abd53556d21e1`; NVD combines the annual and modified feeds with an API update window through the same cutoff. EPSS was scored at `2026-09-09T12:00:22Z`. Optional exploit-index and inferred `attack_classification` fields are omitted from the 2026 refresh; their absence does not establish a negative result.

From the repository root, run `python upload_to_pinecone.py --dry-run` to validate the corpus without using either API. See the [main README](../README.md) for setup and upload instructions.

| File | Records |
| --- | ---: |
| [CVE-1999.json](CVE-1999.json) | 1,540 |
| [CVE-2000.json](CVE-2000.json) | 1,236 |
| [CVE-2001.json](CVE-2001.json) | 1,537 |
| [CVE-2002.json](CVE-2002.json) | 2,357 |
| [CVE-2003.json](CVE-2003.json) | 1,504 |
| [CVE-2004.json](CVE-2004.json) | 2,644 |
| [CVE-2005.json](CVE-2005.json) | 4,627 |
| [CVE-2006.json](CVE-2006.json) | 6,995 |
| [CVE-2007.json](CVE-2007.json) | 6,458 |
| [CVE-2008.json](CVE-2008.json) | 7,005 |
| [CVE-2009.json](CVE-2009.json) | 4,921 |
| [CVE-2010.json](CVE-2010.json) | 5,074 |
| [CVE-2011.json](CVE-2011.json) | 4,646 |
| [CVE-2012.json](CVE-2012.json) | 5,488 |
| [CVE-2013.json](CVE-2013.json) | 6,221 |
| [CVE-2014.json](CVE-2014.json) | 8,427 |
| [CVE-2015.json](CVE-2015.json) | 8,111 |
| [CVE-2016.json](CVE-2016.json) | 9,365 |
| [CVE-2017.json](CVE-2017.json) | 14,760 |
| [CVE-2018.json](CVE-2018.json) | 16,188 |
| [CVE-2019.json](CVE-2019.json) | 16,093 |
| [CVE-2020.json](CVE-2020.json) | 19,386 |
| [CVE-2021.json](CVE-2021.json) | 22,586 |
| [CVE-2022.json](CVE-2022.json) | 26,425 |
| [CVE-2023.json](CVE-2023.json) | 30,597 |
| [CVE-2024.json](CVE-2024.json) | 38,388 |
| [CVE-2025.json](CVE-2025.json) | 43,176 |
| [CVE-2026.json](CVE-2026.json) | 54,862 |
| [rejected.json](rejected.json) | 868 |

**Total:** 370,617 searchable records plus 868 rejected records kept separately (27 from 1999–2025 and 841 from 2026).
