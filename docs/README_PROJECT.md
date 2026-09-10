# PROJECT_3_IFN_I

## Project
Type I Interferon Immunotherapy Response — Single-Cell RNA-Seq Analysis

## Project structure

- `data/` — 10x Genomics input data for HD1, HD2, and P1–P8
- `scripts/` — computational analysis scripts (01–13 plus 06b)
- `results/` — AnnData objects and tabular analysis outputs
- `figures/` — generated figures
- `docs/` — project documentation and results summary
- `notebooks/` — currently empty; the reproducible workflow is implemented in Python scripts
- `logs/` — currently empty
- `requirements.txt` — Python package requirements
- `.venv/` — project Python virtual environment

## Analysis workflow

1. Validate 10x data
2. Load and combine samples
3. Quality control and filtering
4. Normalization and highly variable gene selection
5. PCA, neighbors, UMAP, and Leiden clustering
6. Cluster marker-gene analysis
7. Full-gene marker analysis
8. Marker visualization
9. Cell-type annotation
10. Transcriptomic IRC scoring
11. T-cell IRC validation
12. IRC_High vs IRC_Low differential expression
13. Hallmark GSEA
14. T-cell subtype-specific IRC validation

## Current analysis status

The planned computational workflow is complete. The final dataset contains 94,513 cells and 31,120 genes after QC. Leiden clustering identified 32 clusters (0–31). The T-cell analysis contains 20,315 cells.

## Important methodological note

The IRC used here is a Scanpy transcriptomic gene-set score based on BST2, EIF2AK2, ISG15, MX1, IFIT3, and IRF7. It is a computational transcriptomic proxy and is not identical to the experimental protein-based IRC measurement described in the primary paper.

## Important interpretation note

IRC_High/IRC_Low status is derived from the six-gene IRC signature. Therefore, differential expression of those same signature genes is partly circular and should not be presented as independent validation.

Clinical prediction of anti-PD-1 response was not directly tested by the current pipeline.
