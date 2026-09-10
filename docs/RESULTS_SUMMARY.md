# Results Summary — Project 3: Type I Interferon Immunotherapy Response

## 1. Dataset and Quality Control

The dataset consisted of PBMC single-cell RNA-seq data from 2 healthy donors (HD1 and HD2) and 8 cancer patients (P1–P8). Following quality-control filtering based on detected genes, mitochondrial transcript percentage, and hemoglobin transcript percentage, **94,513 cells and 31,120 genes** remained for downstream analysis.

Cells were retained when they had at least **300 detected genes**, mitochondrial transcripts below **15%**, and hemoglobin transcripts below **5%**. Genes detected in fewer than **5 cells** were removed. Ribosomal gene percentages were calculated for QC assessment but were not used as a filtering criterion.

## 2. Normalization, Dimensionality Reduction and Clustering

The filtered expression matrix was normalized to a total of **10,000 counts per cell**, followed by log transformation. The **2,500 highly variable genes** were selected for dimensionality reduction and clustering.

Principal component analysis was performed using 30 principal components, followed by construction of a nearest-neighbor graph using **20 neighbors**. UMAP was then generated and Leiden clustering was performed at a resolution of **1.0**.

This identified **32 Leiden clusters (clusters 0–31)**.

The resulting clusters represented major immune populations including T cells, NK cells, B cells, myeloid/APC populations, dendritic cells, plasmacytoid dendritic cells, platelets, and a small cycling population. Several clusters were retained as mixed or uncertain because their marker profiles did not allow confident assignment.

## 3. Cell-Type Annotation

Marker-gene analysis using the Wilcoxon method was used to characterize the Leiden clusters. The final annotation included:

- Naive/resting T cells
- Naive/memory T cells
- Memory CD4/GZMK T cells
- Treg-like/activated CD4 T cells
- Cytotoxic T/NK populations
- Cytotoxic NK/T populations
- NK cells
- B cells
- Myeloid and myeloid/APC populations
- Dendritic/APC cells
- pDC-like cells
- Platelets
- Cycling/proliferating cells
- IFN-stimulated myeloid cells
- Mixed/uncertain and unclear/rare populations

Annotation confidence was classified as high, moderate, or low according to the cluster-level marker interpretation.

## 4. Transcriptomic IFN-I Response Capacity Score

To investigate IFN-I responsiveness, a six-gene signature was used:

**BST2, EIF2AK2, ISG15, MX1, IFIT3, and IRF7.**

A Scanpy `score_genes` score was calculated for each cell. Importantly, this represents a **transcriptomic gene-set score derived from the scRNA-seq data**. It is not identical to the experimental protein-based IRC measurement used in the original publication.

Among the annotated populations, the highest mean IRC score was observed in the **IFN-stimulated myeloid population**, followed by the myeloid/T-cell mixed population and pDC-like cells. Among the defined T-cell populations, the mean IRC score was highest in **Cytotoxic T/NK cells**, followed by Cytotoxic NK/T and Memory CD4/GZMK T cells.

## 5. T-Cell IRC Stratification

The analysis focused subsequently on six T-cell populations, yielding **20,315 T cells**:

| T-cell subtype | Total cells | IRC High | IRC Low |
|---|---:|---:|---:|
| Naive/resting T | 9,105 | 4,468 | 4,637 |
| Naive/memory T | 2,135 | 968 | 1,167 |
| Memory CD4/GZMK T | 1,357 | 716 | 641 |
| Treg-like/activated CD4 T | 1,826 | 816 | 1,010 |
| Cytotoxic T/NK | 3,201 | 1,755 | 1,446 |
| Cytotoxic NK/T | 2,691 | 1,435 | 1,256 |
| **Total** | **20,315** | **10,158** | **10,157** |

For the T-cell analysis, cells were divided into IRC_High and IRC_Low using the **median IRC score within the T-cell population**.

## 6. Differential Expression Between IRC_High and IRC_Low T Cells

Wilcoxon differential-expression analysis identified **354 genes with FDR < 0.05** between IRC_High and IRC_Low T cells.

Of these:

- **285 genes** showed higher expression in IRC_High cells.
- **69 genes** showed higher expression in IRC_Low cells.

The strongest differential signals included **EIF2AK2, BST2, MX1, and ISG15**, together with other interferon-associated genes such as **STAT1, PARP14, XAF1, IFI44, and IRF7**.

However, this result must be interpreted carefully: the six core IRC genes were **used to construct the IRC score itself**. Therefore, their strong differential expression between IRC_High and IRC_Low cells is expected and should **not be presented as independent validation** of the IRC classification.

## 7. GSEA of IRC-Associated Transcriptional Programs

Gene-set enrichment analysis was performed using the Hallmark gene sets, with genes ranked according to the **Wilcoxon test statistic**.

Several pathways were significantly enriched in IRC_High cells:

| Hallmark pathway | NES | FDR |
|---|---:|---:|
| **Interferon Alpha Response** | **1.882** | **<0.001** |
| **Interferon Gamma Response** | **1.834** | **<0.001** |
| Allograft Rejection | 1.614 | 0.007 |
| Oxidative Phosphorylation | 1.565 | 0.012 |
| Myc Targets V1 | 1.481 | 0.035 |

The strongest enrichment was observed for the **Interferon Alpha Response** pathway, which is particularly consistent with the biological objective of examining type-I-interferon-associated transcriptional activity.

No significant negatively enriched Hallmark pathways were identified in the reported significant-results output.

## 8. Subtype-Specific IRC Validation

IRC_High versus IRC_Low differential expression was additionally evaluated separately within each T-cell subtype.

All six T-cell subtypes showed significant differential expression of multiple IRC signature genes, with the detected IRC genes consistently showing higher expression in the IRC_High group.

The number of significant genes varied substantially among subtypes:

- Naive/resting T: **361**
- Naive/memory T: **4**
- Memory CD4/GZMK T: **4**
- Treg-like/activated CD4 T: **14**
- Cytotoxic T/NK: **16**
- Cytotoxic NK/T: **4**

This subtype-specific analysis supports the **consistency of the IRC-associated transcriptional signal across T-cell populations**, although the significance of the six IRC genes themselves remains partly circular because they were used to define the IRC status.

## 9. Overall Interpretation

Overall, the analysis identified a diverse PBMC immune landscape comprising **32 Leiden clusters**, with **20,315 T cells** subsequently evaluated for IFN-I response capacity. The transcriptomic IRC score revealed variation in IFN-associated gene expression across immune and T-cell populations.

Within T cells, IRC_High cells showed a transcriptional profile strongly enriched for interferon-related programs. In particular, significant enrichment of the **Hallmark Interferon Alpha Response** pathway provides transcriptomic evidence consistent with increased type-I-interferon-associated activity in the IRC_High population.

The analysis therefore supports the project hypothesis that **pre-existing differences in IFN-I-associated transcriptional activity can be detected at single-cell resolution**, while recognizing that the present IRC score is a computational transcriptomic proxy rather than the experimental protein-based IRC measurement from the original study.

### Important Limitation

The current pipeline does not by itself demonstrate that IRC status predicts actual clinical response to anti-PD-1 therapy. Establishing that relationship would require appropriate patient-level clinical response/outcome data and an analysis connecting IRC measurements to those outcomes.

---

## Notes for Final Report Preparation

1. The actual analysis produced **32 Leiden clusters (0–31)**, rather than the approximately 39 clusters mentioned as an expectation in the mentor guide.
2. The global IRC score was generated using `sc.tl.score_genes` with the six-gene signature. The later T-cell analysis used a **T-cell-specific median cutoff**.
3. The IRC score should be described as a **transcriptomic proxy** and not as the experimental protein-based IRC measurement from the original paper.
4. Differential expression of the six IRC genes is partly circular because those genes define the IRC score.
5. Clinical prediction of anti-PD-1 response was **not directly tested** in this pipeline.
6. GSEA used the **Wilcoxon score** as the ranking statistic, not log2 fold change.
