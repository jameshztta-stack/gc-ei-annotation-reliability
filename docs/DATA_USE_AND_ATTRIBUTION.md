# Spectral data sources and reuse conditions

This document distinguishes the MIT licence covering the software source code from the conditions governing third-party spectral databases. It records the information confirmed from publisher pages on 15 October 2026; **it does not assert that the rights of all original sources have been cleared**.

| Source | Published access and conditions | Use in this software | Remaining rights assessment |
|---|---|---|---|
| MS-DIAL GC–EI–MS/Kovats-RI source, H. Tsugawa, [DOI 10.5281/zenodo.21910638](https://doi.org/10.5281/zenodo.21910638) | Publicly downloadable 23.1 MB MSP (28,220 records). The Zenodo record's Rights/License section does not show a clearly readable licence grant in the publicly retrieved page. | Current reference prepared locally after matching the original SHA-256; original publisher peak arrays are not stored in GitHub. | **Unresolved:** confirm with the depositor that this source and any included subcollections permit the current hosted computational service, redistribution of source-derived items if any, and proposed future publication reuse. |
| SWGDRUG EI spectral library v3.14, [publisher library page](https://swgdrug.org/ms.htm) | Publisher offers free download; spectra were compiled from several contributing organizations and are reviewed under a NIST QA protocol. A general licence granting redistribution or commercial rights is not established from that page. | Used as a separately selected 370-spectrum retrospective source-label evaluation; original spectra are **not bundled** with this repository. | **Unresolved:** confirm permitted redistribution of spectrum-derived outputs and any commercial use with custodians. Read and cite original library notices. |
| RECETOX Exposome HR-[EI+]-MS v2, [DOI 10.5281/zenodo.14285896](https://doi.org/10.5281/zenodo.14285896) | The publisher explicitly describes the library as **CC-BY-NC** (attribution, noncommercial). Its original spectra are from authentic compounds measured on GC–Orbitrap instrumentation. | Used for 96 historically selected retrospective source-label cases. No original MSP peaks redistributed in this repository. | **Do not assume commercial reuse is permitted.** If redistribution, hosted commercial use or adaptation triggers licence restrictions, obtain permission or exclude the affected source. |
| Project-generated scientific software | MIT licence in the repository | Publicly available source code | MIT does **not** override the databases' licences. |

## Source chemistry and permissions

The source-quality inventory examined **13,111** retained EI spectral fingerprints. The original MSP included a nonempty `LICENSE` text field for **11,992** and lacked one for **1,119**. Source-level fields often contain inconsistent wording (including CC BY-SA references); this does not establish one uniform licence for the entire compiled MSP. A missing field is **neither permission nor evidence of infringement**.

The current code recreates the 8,455-reference search matrix locally from the originally published MSP, rather than shipping its peak arrays. This reduces republication concerns but does **not** alone settle whether each source permits the software's intended mode of use. The derived 1,410/609/466 research CSV files contain study-generated features, labels and results, not reference-library peak lists; they should still be considered in final provenance and licence review because they were computed from third-party spectra.

### Permissions outstanding

1. Confirm the MS-DIAL deposited file's applicable corpus/subcollection licensing with the source depositor or authoritative source documentation.
2. Confirm SWGDRUG terms relevant to distributing derived numerical evidence and using source spectra in research software.
3. Honor RECETOX's CC-BY-NC conditions; secure appropriate permission for any commercial context.
4. Cite all three source collections in study-specific reporting. Do not replace original dataset citations with the software DOI.
5. Retain a written record of permissions or licence determinations. This is a rights-holder question; it cannot be resolved through an automated statistical test.

**Software DOI:** https://doi.org/10.5281/zenodo.23373447 is the preceding software release; a later release obtains its own DOI only after the publishing platform confirms deposition.
