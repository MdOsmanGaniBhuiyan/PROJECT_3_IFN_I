# Project 3 IFN-I — Final Figure Organization

## Main figures

### Figure 1. Quality-control overview
`Figure_1_QC.png`
QC distributions before filtering for healthy-donor and patient cells. Metrics shown are number of genes detected, total counts, mitochondrial percentage, ribosomal percentage, and hemoglobin percentage.

### Figure 2. Global cell landscape and annotation
- `Figure_2A_UMAP_Leiden_clusters.png` — Leiden clusters (32 clusters, labels 0–31).
- `Figure_2B_UMAP_annotated_cell_types.png` — manually assigned cell-type annotations.

### Figure 3. Marker-based annotation validation
`Figure_3_marker_dotplot.png`
Dot plot showing canonical marker-gene expression across Leiden clusters. Dot size represents the fraction of cells expressing the marker and dot intensity represents mean expression.

### Figure 4. Transcriptomic IFN-I response capacity (IRC) landscape
- `Figure_4A_IRC_score_UMAP.png` — continuous IRC gene-set score.
- `Figure_4B_IRC_status_UMAP.png` — IRC_High versus IRC_Low classification.
- `Figure_4C_IRC_score_by_cell_type.png` — IRC score distributions across annotated cell types.

The IRC score here is a transcriptomic Scanpy `score_genes` score based on BST2, EIF2AK2, ISG15, MX1, IFIT3, and IRF7. It is not the experimental protein-based IRC measurement from the original paper.

### Figure 5. T-cell IRC analysis
- `Figure_5A_Tcell_IRC_status_UMAP.png` — T-cell IRC_High/IRC_Low status.
- `Figure_5B_Tcell_IRC_score_by_subtype.png` — score distributions across six T-cell subtypes.

## Supplementary figures

- `Figure_S1_HVG_selection.png` — highly variable gene selection.
- `Figure_S2_PCA_variance_ratio.png` — PCA variance-ratio diagnostic.
- `Figure_S3_UMAP_by_sample.png` — sample distribution across UMAP.

## Important reporting notes

1. The Leiden analysis contains 32 clusters (0–31).
2. The final T-cell analysis contains 20,315 cells; the T-cell-specific IRC median split produced 10,158 IRC_High and 10,157 IRC_Low cells.
3. The IRC score is relative and can be negative; it should not be described as a percentage.
4. Differential expression and subtype validation include genes used to construct the IRC signature, so those genes are not independent validation of the score.
5. The analysis did not perform patient-level clinical response prediction.


## GSEA update
The five FDR-significant Hallmark enrichment plots supplied with the project are assembled into Figure 6. All 15 supplied individual GSEA PDFs are retained under the supplementary GSEA folder.
