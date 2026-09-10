import scanpy as sc
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------
INPUT = "results/adata_pca_umap_leiden.h5ad"
OUTPUT_H5AD = "results/adata_full_gene_markers.h5ad"
OUTPUT_CSV = "results/full_gene_marker_genes.csv"
OUTPUT_TOP20 = "results/full_gene_top20_markers.csv"

# --------------------------------------------------
# Create output directories
# --------------------------------------------------
Path("results").mkdir(exist_ok=True)

# --------------------------------------------------
# Load data
# --------------------------------------------------
print(f"Loading: {INPUT}")
adata = sc.read_h5ad(INPUT)

print(f"Loaded dataset: {adata.n_obs:,} cells × {adata.n_vars:,} genes")

# --------------------------------------------------
# Check required information
# --------------------------------------------------
if "leiden" not in adata.obs:
    raise ValueError("Leiden clusters not found in adata.obs")

print("\nLeiden clusters:")
print(adata.obs["leiden"].value_counts().sort_index())

# --------------------------------------------------
# Rank marker genes using ALL genes
# --------------------------------------------------
print("\nRunning Wilcoxon marker analysis using ALL genes...")

sc.tl.rank_genes_groups(
    adata,
    groupby="leiden",
    method="wilcoxon",
    use_raw=False,
    n_genes=adata.n_vars
)

print("Marker analysis completed.")

# --------------------------------------------------
# Extract results
# --------------------------------------------------
result = sc.get.rank_genes_groups_df(
    adata,
    group=None
)

# Remove genes with missing names
result = result.dropna(subset=["names"])

# Save complete marker table
result.to_csv(OUTPUT_CSV, index=False)

print(f"\nSaved full marker table:")
print(OUTPUT_CSV)

# --------------------------------------------------
# Top 20 markers per cluster
# --------------------------------------------------
top20 = (
    result
    .sort_values(["group", "pvals_adj", "scores"])
    .groupby("group", observed=False)
    .head(20)
)

top20.to_csv(OUTPUT_TOP20, index=False)

print(f"Saved top-20 marker table:")
print(OUTPUT_TOP20)

# --------------------------------------------------
# Save AnnData
# --------------------------------------------------
adata.write(OUTPUT_H5AD)

print(f"\nSaved AnnData:")
print(OUTPUT_H5AD)

print("\nDONE.")
