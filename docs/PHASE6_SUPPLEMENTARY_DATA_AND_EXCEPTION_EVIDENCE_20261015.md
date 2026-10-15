# Supplementary Information — GC–EI–MS Annotation Tool

These supplementary notes describe the spectral sources, chemical-data quality controls, model specification and software evaluation for the **GC–EI–MS Annotation Tool (version 2.0.2)**. Original third-party spectral peak arrays are not redistributed. The publisher-label evaluations are retrospective and must not be interpreted as independent experimental confirmation of chemical identity.

## SI-1 — Version, source and immutable scientific design

| Resource / role | Exact value | Verifiable archival location |
|---|---|---|
| MS-DIAL public MSP raw records | **28,220**, SHA-256 `a1035f8d6c4e717e5fe086f11baadb5f5d44bec3d98d68c7415a1295ae304a70` | Tsugawa public MS-DIAL Zenodo record `https://doi.org/10.5281/zenodo.21910638`; `gcei/reference_builder.py` |
| Original cleaned nominal EI fingerprints | **13,111**, one per retained fingerprint | `audits/v2_full13111_source_chemistry_20261014/v2_all13111_retained_spectra_chemical_identity_source_integrity_report.json` at source research commit `9d5c57a44e57d3eed94c82930c2868e451573676` |
| Corrected research v2 retrieval reference | **8,455** first14 InChIKey connectivity identities, SHA `2d7e66be8ad2c93aa08eefc0cd54a25c1c1788502856a35fcedb49cb84759a01` | `models/v2/reference_index.csv`, `models/v2/release_manifest.json` |
| Original query-capable distinct first14 groups | **2,019** (1,410 developer + 609 once-reserved); all original 609 source labels are in the reference; query and reference from shared MS-DIAL archive | `docs/V2_609_ONE_SHOT_FINAL_WITHIN_SOURCE_RESULTS_INDEPENDENT_REVIEWER_AUDIT_20261014.md` |
| Original development roles | **1,410** development observations organized into four previously defined subsets (201, 383, 403 and 423) | Original source and development-role records; no newly independent evaluation |
| fixed HGB original fit | scikit-learn HistGradientBoostingClassifier; **12 exact ordered features**; SHA `a9370828084881072307fe081f3ecc34e400d26c6710c8a542bbad0bad0ccf13` | `models/v2/release_manifest.json` |
| Original within-source one-use evaluation | **609** SHA `62899a9be61118299e730558fe097e61e7423411d6ea33ea678245f282b41dd7`; already evaluated; not a newly independent test | `audits/v2_609_one_shot_within_msdial_20261014/v2_609_single_use_within_msdial_per_query.csv`, archived commit |
| Separate selected publisher source retrieval | **466** = 370 SWGDRUG v3.14 + 96 RECETOX; 419 unique source first14; SHA `09a228acbf93fb307b9150ff47024c253e4e94ea4223f8cc309fc8083afdc11b`; previously evaluated | `audits/v2_retrospective_cross_library_20261014/v2_466_retrospective_cross_library_model_and_retrieval_predictions.csv` |
| v2 public web software | Streamlit v2.0.2, GitHub MIT software licence, Zenodo software DOI `10.5281/zenodo.23373447` | `https://gc-ei-annotation.streamlit.app/`; `app.py` |

## SI-2 — Source chemistry exception matrix

**Do not interpret structural encoding agreements as authenticated experimental chemical structures; prespecified curation originally enforced first14/formula consistency.**

| Evidence class | Actual archival count | Handling and remaining limitation |
|---|---:|---|
| Retained unique nominal EI spectra | **13,111** | Full source membership replayed with original SHA; repeated raw spectra collapsed |
| Retained first14 groups with >1 distinct recreated Standard full InChIKey | **294** | Connectivity agreement can conflate stereochemistry/chemical representation. **119** of these groups lack any other retained spectrum with exactly the fixed reference's Standard full key; full-key exact identification is OUT OF SCOPE |
| Retained original source-name soft semantic flags | **373** | Nonexclusive qualifiers: **313** derivative-keyword; **57** minor-component; **1** isomer; **2** tentative/similarity. Their presence does not itself prove wrong molecular structure |
| Retained original versus recreated advanced InChIKey-layer discrepancy | **6 source-spectrum rows** spanning **4 unique first14 connectivity groups** | Original source rows **3196, 3426, 5384, 7781, 11277, 11278**; connectivity and formula agree but non-connectivity layer cannot be adjudicated; keep source flags |
| Advanced-key discrepancies among 8,455 reference representatives | **4 unique reference identities** | All independently checked; no altered first14 label and no stereochemical proof |
| Raw original exact-spectrum fingerprint spanning conflicting source first14 labels | **1 group containing four raw rows** | Original rows 1073, 1799, 15077, 15803; retained row **1799** has structure/first14 support under predefined curation; unsupported keys excluded. This is a curation resolution, **not** authentic-standard proof |
| Retained source InChIKey/SMILES first14 and formula screened consistency | **13,111 compliant by eligibility filter** | This is **not** an independently measured zero chemical-label-error rate |

**Official existing machine-readable archival evidence:**
- `audits/v2_full13111_chemical_exceptions_20261014/v2_13111_chemical_exceptions_and_name_provenance_review.json` (complete 6-case list, one 4-row collision, 294/373 flags).
- `audits/v2_full13111_chemical_exceptions_20261014/v2_294_within_connectivity_advanced_structure_heterogeneity.csv`.
- `audits/v2_original_reference_four_advanced_keys_20261014/v2_frozen8455_four_advanced_inchikey_exceptions_independent_reaudit.json`.
- `docs/V2_COMPLETE_13111_RETAINED_SPECTRA_CHEMISTRY_AND_REVIEWER_ISSUES_20261014.md`.

## SI-3 — Acquisition lineage and data licence *not* assumed resolved

Full original retained MSP field inventory `audits/v2_13111_acquisition_provenance_20261014/v2_13111_source_provenance_field_inventory.json`:

- **13,111/13,111** had source-reported name, formula, SMILES, InChIKey, RETENTIONINDEX and positive IONMODE; original GC–EI source convention, no matched prospective instrument experiment.
- `COLLISIONENERGY` field `70eV` on **12,900/13,111**; no assertion that the same verified instrument settings applied to every case.
- `INSTRUMENTTYPE` only **211/13,111**, listing `GC-EI-TOF`; `COMMENT` 211/13,111 indicating FiehnVolatile library accession, not instrument run.
- `LICENSE` metadata for **11,992/13,111**, primarily non-normalized CC BY-SA phrases; **1,119** retained rows missing original licence field. A per-record `LICENSE` field is not permission to redistribute the whole collection under the software's MIT license. Obtain origin/licensing review if distributing source-derived spectra or deploying under incompatible commercial terms.
- Original MSP contains **no confirmed laboratory/raw-file/instrument serial/authentic-standard lot** trace in the available record fields. **Zero individually verified independent acquisition lineages** established by the existing source audit.
- SWGDRUG/RECETOX is publisher-separated by collection, but accession-level original measurement independence from MS-DIAL source, reuploads and cross-library aliases are not authenticated. SWGDRUG public library chemistry review and RECETOX authentic-standard collection documentation are valuable *collection-level evidence*, not an individual specimen chain-of-custody proof.
- The old 609 internal MS-DIAL query/reference spectra may differ as records or exact nominal fingerprints but **share published source archive**, a critical within-source interpretation restriction.
- Source-licensing/access source reference: `https://zenodo.org/records/21910638`; SWGDRUG `https://swgdrug.org/ms.htm`; RECETOX `https://zenodo.org/records/14285896`. A licence audit of redistribution and monetization remains an external compliance gate.

## SI-4 — Endpoints, numbers, and honest error controls

- Correct label = matching **publisher-reported InChIKey first14** of the correct archived source reference, **not** authenticated whole-molecule, specimen identity, stereoisomer, derivative, mixed-feature deconvolution, or chromatographic peak assignment.
- Original 609: top1 **394/609** (64.70%); top5 **489/609**, top10 **509/609**. Wrong first hits **215/609**; source label ranks: 1 **394**; 2–5 **95**; 6–10 **20**; >10 **100**.
- Previously exposed, selection-filtered 466: top1 **334/466** (71.67%), first14 at ranks 2–5 **67**, 6–10 **6**, >10 **59**; incorrectly ranked top1 **132**, with **50 same formula** as the publisher label (possible constitutional/isomer/formula ambiguities) and **82 different formula**. Formula agreement is not proof of isomers or causal error origin.
- Original 609 HGB correctness discrimination AUROC **0.863304**; margin-only **0.812679**, cosine-only **0.706682**. HGB Brier **0.140645**, 10-bin ECE **0.044938** on descriptive source labels. AUROC neither changes top1 ranks nor certifies chemical authenticity.
- Original 1,410 exposed dev OOF: 12f HGB Brier **0.14416** vs 12f logistic **0.14675**; modest difference without convincing architecture superiority. Original 609 K=198 HGB-selected wrong **12**, margin-selected wrong **11**. Disclose the unfavorable cases.
- Fixed original 10%-target `p>=0.87`: 609 **198 accepted / 12 wrong**; 466 **185 accepted / 12 wrong**. Fixed 5%-target `p>=0.94 AND margin>=0.20`: 609 **38 accepted / 0 wrong**; 466 **25 accepted / 0 wrong**. **Neither is prospectively certified**; no 5%/10% *actual future error* guarantee.
- All 609 labels deliberately in current reference; out-of-library or novel-chemical rejection not tested. v2 is **EI-only** with **no RI fusion and no valid v1 conformal carryover**.

## SI-5 — Current software and independent computational checks

- Source and model SHA checks at initialization and source rebuild; 12-feature fixed HGB only **scores correctness of existing top1**, does **not** re-rank candidates.
- `app.py`: public browser-based Streamlit single and batch CSV, top10 *single-query* candidate display, HGB score, top-two margin, historical uncertified rules, source/version provenance CSV and disclaimer.
- **Important nuance**: current batch summary export supplies **one top1 row per spectrum**, **not** a 10-per-spectrum batch candidate matrix. The 12×10 candidate matrix used for software verification was extracted through individual engine calls, **not a button labelled "batch top10 export"**. Do not assert the public UI has batch top10 export unless newly implemented and independently tested. (For each single spectrum, top10 candidate CSV download is present.)
- Independent same-case numerical evaluation and figures completed: GitHub Actions `38606816850`, original historical ledgers and SHA checks.
- Twelve existing botanical example EI input checks completed: GitHub Actions `38607229807`.
- Synthetic software input and integrity tests (**13 passed**): GitHub Actions `38609096672`.
- Review-routing and twelve-example software checks completed: GitHub Actions `38618746013`; output artefact `11920099614`. 12 existing **unlabelled** example spectra, 120 engine candidate records; not a biological result.
- The current `app.py` passed **two** headless Streamlit interface tests: GitHub Actions `38619103980`. Headless tests not live browser accessibility/usability or server uptime proof.

## SI-6 — Reproducible material, citation rights and known work still open

- fixed public software and current v2 scientific model: `https://github.com/jameshztta-stack/gc-ei-annotation-reliability` and software DOI `https://doi.org/10.5281/zenodo.23373447` (software publication does not itself confirm analytical accuracy).
- Original computational research commit `9d5c57a44e57d3eed94c82930c2868e451573676`; research code `https://github.com/jameshztta-stack/gc-ei-annotation-reliability/pull/8` unmerged as of writing.
- The manuscript should disclose that the source data must be fetched under original publisher rights, byte verified and processed locally; scripts cannot conjure inaccessible upstream records, and upstream licensing requires an independent compliance read.
- Material supplements should include a data availability and code availability statement, **qualified role/split tables**, full chemical exceptions and handling logic, complete source metadata coverage, pre-fixed historical acceptance definitions, complete source outcome tables/uncertainty curves and Figure/SI registry.
- **Citation before publication:** cite the existing open-source software DOI and upstream data provider correctly. Do not invent a published manuscript DOI.
- **Remaining limitations and preparation requirements:** a complete independent human scientist code/data audit, original data licensing clearance and a clear substantive advance beyond previously published GC–EI reliability software if the intended journal requires major innovation. Independent experimental confirmation was not part of this computational study.

**The supplementary results are derived from existing source records and verified computational analyses; they are not new laboratory measurements.**
