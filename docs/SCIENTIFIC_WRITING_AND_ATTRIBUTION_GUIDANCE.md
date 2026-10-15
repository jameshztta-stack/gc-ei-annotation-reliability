# Scientific writing, references and software reporting conventions

Use this guidance for the GC–EI–MS research article, supplementary information, figures, abstract, cover letter and subsequent revisions. The primary submission documents are the GC–EI–MS manuscript and its corresponding Supplementary Information.

## Scientific writing

- Describe the single current public software release, **GC–EI–MS Annotation Tool v2.0.2**. Do not recount earlier application releases, interface iterations or development sessions unless a genuinely indispensable technical point requires it.
- Use direct scientific language. Prefer **defined reference library**, **specified model**, **reproducible results**, **source-data quality assessment**, **documented data provenance**, **confidence screening** and **version identification** over internal engineering labels or promotional claims.
- Use naturally constructed sentences in the authors' scientific voice. Avoid marketing adjectives, unqualified uniqueness claims and claims that a tool is more effective than existing software without actual matched evidence.
- Identify scientific method/data roles and disclose that the 609 and 466 case outcomes have already been evaluated. This is scientifically necessary; it is independent of the software release history.
- Maintain only the implemented current capabilities. Current v2.0.2 **does not use RI in scoring**, classify absent-library compounds, verify full stereochemistry or certify prospective 5%/10% error rates. The web UI currently offers a top-ten candidate export for a single query and a first-hit summary for a batch.
- Preserve full numerical denominators and unfavorable findings, including cases where the top-two similarity margin performs better at a specified acceptance level.

## Attribution to previous work

- Cite **Stein & Scott (1994)** for established mass/intensity-weighted library search methods: https://doi.org/10.1016/1044-0305(94)87009-8 .
- Cite **Stein (1994)** for probabilities of correct spectral library matches and the distinction between in-library reliability and unknown reference coverage: https://doi.org/10.1016/1044-0305(94)85022-4 .
- Cite **Kim and Zhang (2015)** for the top-one/top-two similarity-difference strategy in GC–MS metabolomics: https://doi.org/10.1002/cem.2665 .
- Cite **McGlynn et al. (2025)** for contemporary GC–EI–MS candidate-identification methods incorporating uniqueness, ubiquity, source information and RI: https://doi.org/10.1021/jasms.4c00451 .
- Further prior publications—including matchms, FastEI, LLM4MS and modern probability/RI tools—must be credited in their relevant contexts.
- Do not reproduce distinctive phrases, figures, tables or workflows from source papers as original material; independently write explanations and cite the sources where their concepts, evidence or data are discussed. Source citation and independent writing reduce plagiarism risks but do not themselves establish originality or guarantee editorial acceptance.

## Specific contribution being investigated

The manuscript concerns a **GC–EI library annotation application integrating documented source chemistry checks, conventional spectral matching, a separately evaluated correctness estimator, uncertainty disclosure, and a web interface with reproducible outputs**. This combination is the subject of our claimed contribution. Do not claim to have invented probability-of-match, cosine matching, two-score margins or web interfaces, nor imply that this combination is unique across all prior applications without a comprehensive comparative basis.

## Statistical and chemistry boundaries

The first14 reference outcome refers to **agreement with published database connectivity labels** in a selected in-reference analysis, not the independently confirmed chemical composition of an unknown specimen. The software's HGB score does not reorder the candidates. Both evaluated 5%/10% historical thresholds lack certified future error guarantees. Keep all limitations visible in the abstract, Methods, Results, figure legends and discussion as appropriate.

## Submission practice

Cite the original MS-DIAL source DOI `10.5281/zenodo.21910638` and software v2.0.2 DOI `10.5281/zenodo.23373447`. Keep original data and software licences distinct. Include exact study/software identifiers as required for reproduction without turning the manuscript into a developer change log. Complete verified author contributions, institutional details, funding and disclosure statements before submission.

**Article readiness must be judged from demonstrated scientific value and source-supported findings, not from numeric originality ratings or language promising guaranteed acceptance.**
