# Final Figure Captions — Project 3 IFN-I

**Figure 1. Quality-control overview.** Violin distributions of QC metrics before filtering for healthy-donor and patient cells: genes detected, total counts, mitochondrial percentage, ribosomal percentage, and hemoglobin percentage. Cells were subsequently filtered using the predefined thresholds in the analysis pipeline.

**Figure 2. Global cell landscape and cell-type annotation.** (A) UMAP representation of 94,513 retained cells colored by 32 Leiden clusters (0–31). (B) UMAP colored by manual cell-type annotations based on canonical marker genes.

**Figure 3. Marker-based annotation validation.** Dot plot of canonical marker genes across Leiden clusters. Dot size represents the fraction of cells expressing each marker, while color intensity represents mean expression.

**Figure 4. Transcriptomic IFN-I response capacity across the PBMC landscape.** (A) Continuous Scanpy gene-set score based on BST2, EIF2AK2, ISG15, MX1, IFIT3, and IRF7. (B) IRC_High versus IRC_Low classification using the global median cutoff. (C) Score distributions across annotated cell types. This transcriptomic score is distinct from the experimental protein-based IRC measurement described in the reference paper.

**Figure 5. IFN-I response capacity in T-cell populations.** (A) T-cell UMAP colored by Tcell_IRC_status. (B) IRC score distributions across six annotated T-cell subtypes. T-cell IRC status was defined using the T-cell-specific median cutoff.

**Figure 6. Hallmark pathway enrichment in IRC_High T cells.** Ranked enrichment analysis using the Wilcoxon score as the gene-ranking statistic. Significant pathways (FDR < 0.05) include interferon alpha response, interferon gamma response, allograft rejection, oxidative phosphorylation, and Myc targets V1.

**Supplementary Figure S1.** Highly variable gene selection diagnostic.

**Supplementary Figure S2.** PCA variance-ratio diagnostic for the first 30 principal components.

**Supplementary Figure S3.** Distribution of the ten study samples across the UMAP embedding.
