# Third-party data notices

This is a transformed, point-in-time corpus. The repository does not claim ownership of upstream data and does not apply a blanket license to the generated records. Upstream terms continue to govern source-derived portions.

## Included sources

- **CVE Program / CVE List V5** — CVE records, lifecycle, CNA descriptions, affected products, configurations, solutions, workarounds, and references. Copyright © 1999–2026 The MITRE Corporation. CVE is a trademark of The MITRE Corporation. CVE-derived portions are redistributed under the CVE license published in the [CVE Terms of Use](https://www.cve.org/legal/termsofuse), reproduced [below](#cve-program-license) with its disclaimers. Retain this copyright designation and the full license with every copy.
- **NIST National Vulnerability Database (NVD)** — NVD enrichments such as CVSS, CWE, and CPE facts. NIST publications are public domain in the United States. This product uses data from the NVD but is not endorsed or certified by the NVD. See the [NVD terms](https://nvd.nist.gov/developers/terms-of-use) and [NVD FAQ](https://nvd.nist.gov/general/FAQ-Sections/General-FAQs).
- **CISA Known Exploited Vulnerabilities Catalog** — exploitation, remediation deadline, and ransomware-use facts. The official data mirror is released under CC0 1.0. See [CISA KEV data](https://github.com/cisagov/kev-data).
- **FIRST EPSS** — point-in-time EPSS probability and percentile. Attribution: See EPSS at [FIRST](https://www.first.org/epss). Review the [EPSS FAQ](https://www.first.org/epss/faq) before redistribution.
- **ProjectDiscovery Nuclei Templates** — factual template identifiers and source URLs only; no template bodies are included. See the upstream [MIT license](https://github.com/projectdiscovery/nuclei-templates/blob/main/LICENSE.md).
- **Exploit Database** — factual Exploit-DB identifiers and source URLs only; no exploit bodies or copied descriptions are included. See the upstream [license](https://gitlab.com/exploit-database/exploitdb/-/blob/main/LICENSE.md).
- **Rapid7 Metasploit Framework** — factual module identifiers and source URLs only; no module code or copied descriptions are included. Metasploit contains mixed third-party terms; review its [license inventory](https://github.com/rapid7/metasploit-framework/blob/master/LICENSE).
- **PoC-in-GitHub index** — bounded factual repository URLs only; no repository code or copied descriptions are included. The index repository currently shows no project license, and each linked repository has its own terms. See [nomi-sec/PoC-in-GitHub](https://github.com/nomi-sec/PoC-in-GitHub).

## Deliberately excluded

The portable corpus does not emit proprietary VulnCheck service/feed enrichments, Sigma rules, OSV advisory text, CAPEC expansion, ATT&CK mappings, exploit or template bodies, or third-party PoC descriptions. A CVE or NVD record can still contain a VulnCheck-authored CNA description or reference; those portions came through the CVE/NVD sources and remain under their governing terms.

Product names and trademarks belong to their respective owners. Source inclusion does not imply endorsement. Verify current upstream records and terms before republishing or making operational decisions.

## CVE Program license

Source: [CVE Program Terms of Use](https://www.cve.org/legal/termsofuse), verified September 9, 2026.

Copyright © 1999-2026, The MITRE Corporation.

### License

Submissions: For all materials you submit to the Common Vulnerabilities and Exposures (CVE™), you hereby grant to The MITRE Corporation (MITRE) and all CVE Numbering Authorities (CNAs) a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute such materials and derivative works. Unless required by applicable law or agreed to in writing, you provide such materials on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.

CVE Usage: MITRE hereby grants you a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute Common Vulnerabilities and Exposures (CVE™). Any copy you make for such purposes is authorized provided that you reproduce MITRE's copyright designation and this license in any such copy.

### Disclaimers

ALL DOCUMENTS AND THE INFORMATION CONTAINED THEREIN PROVIDED BY MITRE ARE PROVIDED ON AN "AS IS" BASIS AND THE CONTRIBUTOR, THE ORGANIZATION HE/SHE REPRESENTS OR IS SPONSORED BY (IF ANY), THE MITRE CORPORATION, ITS BOARD OF TRUSTEES, OFFICERS, AGENTS, AND EMPLOYEES, DISCLAIM ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE USE OF THE INFORMATION THEREIN WILL NOT INFRINGE ANY RIGHTS OR ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.
