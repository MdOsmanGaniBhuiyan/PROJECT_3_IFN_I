# Final Analysis Validation — PROJECT_3_IFN_I

## Status

The planned computational workflow is complete. The following validation points should be checked before final report submission.

## 1. Dataset and QC

- 10 samples: HD1, HD2, P1–P8.
- Post-QC dataset: 94,513 cells × 31,120 genes.
- Cell filtering: minimum 300 genes, mitochondrial percentage <15%, hemoglobin percentage <5%.
- Genes detected in fewer than 5 cells were removed.
- Ribosomal percentages were calculated but were not used as a filtering criterion.

## 2. Clustering

- 2,500 highly variable genes were used for PCA/clustering.
- 30 PCs were used.
- Neighbors: 20.
- Leiden resolution: 1.0.
- Random state: 42.
- Result: 32 Leiden clusters, numbered 0–31.

## 3. Annotation

The annotations include T-cell, NK, B-cell, myeloid/APC, dendritic/pDC, platelet, cycling, IFN-stimulated myeloid, and uncertain/rare populations.

The annotation script assigns confidence as High, Moderate, or Low. Low-confidence groups should be described cautiously rather than treated as definitive cell identities.

## 4. IRC scoring

The six-gene signature is:
BST2, EIF2AK2, ISG15, MX1, IFIT3, IRF7.

Scanpy `score_genes` was used. The score is transcriptomic and relative; its absolute numerical value should not be interpreted as a percentage or as the experimental protein IRC.

## 5. T-cell analysis

Six T-cell populations were analyzed, totaling 20,315 cells. A T-cell-specific median IRC score was used to define IRC_High and IRC_Low.

Counts:
- IRC_High: 10,158
- IRC_Low: 10,157

## 6. Differential expression

Wilcoxon testing identified 354 genes at FDR <0.05:
- 285 higher in IRC_High
- 69 higher in IRC_Low

The six IRC genes are expected to be strongly associated with IRC status because they define the score. Their differential expression is therefore not independent validation.

## 7. GSEA

Hallmark GSEA identified significant positive enrichment in IRC_High for:
- Interferon Alpha Response: NES 1.882, FDR <0.001
- Interferon Gamma Response: NES 1.834, FDR <0.001
- Allograft Rejection: NES 1.614, FDR 0.007
- Oxidative Phosphorylation: NES 1.565, FDR 0.012
- Myc Targets V1: NES 1.481, FDR 0.035

The Interferon Alpha Response result is the most directly aligned with the project hypothesis.

## 8. Subtype validation

Subtype-specific DE was performed for six T-cell populations. Significant-gene counts were:
- Naive/resting T: 361
- Naive/memory T: 4
- Memory CD4/GZMK T: 4
- Treg-like/activated CD4 T: 14
- Cytotoxic T/NK: 16
- Cytotoxic NK/T: 4

The IRC signature genes detected as significant were consistently higher in IRC_High groups, but this remains partly circular because those genes define the score.

## 9. Final scientific interpretation

The results support detection of variation in IFN-I-associated transcriptional activity at single-cell resolution. IRC_High T cells show strong enrichment of interferon-associated transcriptional programs, especially the Hallmark Interferon Alpha Response pathway.

The analysis does not establish that IRC status predicts clinical anti-PD-1 response because clinical outcome association was not tested in the current pipeline.
