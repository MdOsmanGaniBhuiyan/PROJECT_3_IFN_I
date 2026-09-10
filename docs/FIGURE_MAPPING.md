# Figure Mapping — PROJECT_3_IFN_I

## Main report figures

### Figure 1 — Quality control
File: `qc_violin_before_filtering.png`
Purpose: Show distributions of QC metrics before filtering and motivate the filtering criteria.

### Figure 2 — Global cell landscape
Files:
- `umap_leiden_clusters.png`
- `umap_annotated_cell_types.png`
Purpose: Show the 32 Leiden clusters and their biological annotations.

### Figure 3 — Marker validation
File: `marker_dotplot.png`
Purpose: Demonstrate expression of canonical marker genes across Leiden clusters.

### Figure 4 — IRC landscape
Files:
- `umap_irc_score.png`
- `umap_irc_status.png`
- `irc_score_by_cell_type.png`
Purpose: Show the spatial and cell-type distribution of the transcriptomic IRC score.

### Figure 5 — T-cell IRC
Files:
- `umap_tcell_irc_status.png`
- `tcell_irc_score_by_subtype.png`
Purpose: Show IRC_High/IRC_Low status and score distributions across T-cell subtypes.

## Supplementary figures

- `highly_variable_genes.png`
- `pca_variance_ratio.png`
- `umap_by_sample.png`

These provide methodological and dataset-level context and can be moved to supplementary material if the report has a strict figure limit.

## GSEA

GSEA analysis results already exist in:
`results/gsea/hallmark_gsea_results.csv`

A GSEA visualization is optional; the analysis itself has already been completed and should not be rerun merely for documentation.
