#!/usr/bin/env python3

import scanpy as sc
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

INPUT = "results/adata_pca_umap_leiden.h5ad"
OUTPUT_DIR = Path("results")
FIGURE_DIR = Path("figures")

OUTPUT_DIR.mkdir(exist_ok=True)
FIGURE_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

print(f"Loading: {INPUT}")

adata = sc.read_h5ad(INPUT)

print(
    f"Loaded dataset: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)

# --------------------------------------------------
# 2. Check Leiden clustering
# --------------------------------------------------

if "leiden" not in adata.obs.columns:
    raise ValueError("Leiden clustering not found in adata.obs")

print("\nLeiden clusters:")
print(adata.obs["leiden"].value_counts().sort_index())

# --------------------------------------------------
# 3. Find marker genes
# --------------------------------------------------

print("\nRunning Wilcoxon differential expression...")

sc.tl.rank_genes_groups(
    adata,
    groupby="leiden",
    method="wilcoxon",
    key_added="rank_genes_leiden"
)

print("Marker-gene analysis completed.")

# --------------------------------------------------
# 4. Save complete marker results
# --------------------------------------------------

marker_df = sc.get.rank_genes_groups_df(
    adata,
    group=None,
    key="rank_genes_leiden"
)

marker_file = OUTPUT_DIR / "cluster_marker_genes.csv"

marker_df.to_csv(marker_file, index=False)

print(f"\nSaved complete marker table:")
print(marker_file)

# --------------------------------------------------
# 5. Save top 20 markers per cluster
# --------------------------------------------------

top20 = (
    marker_df
    .groupby("group", sort=False)
    .head(20)
)

top20_file = OUTPUT_DIR / "cluster_top20_markers.csv"

top20.to_csv(top20_file, index=False)

print(f"Saved top 20 markers per cluster:")
print(top20_file)

# --------------------------------------------------
# 6. Print top 10 markers for each cluster
# --------------------------------------------------

print("\n" + "=" * 70)
print("TOP 10 MARKER GENES PER LEIDEN CLUSTER")
print("=" * 70)

for cluster in sorted(adata.obs["leiden"].unique(), key=int):

    genes = (
        marker_df[marker_df["group"] == cluster]
        .head(10)["names"]
        .tolist()
    )

    print(f"\nCluster {cluster}:")
    print(", ".join(genes))

# --------------------------------------------------
# 7. Save updated AnnData
# --------------------------------------------------

OUTPUT_H5AD = OUTPUT_DIR / "adata_markers.h5ad"

adata.write_h5ad(OUTPUT_H5AD)

print("\nSaved AnnData with marker results:")
print(OUTPUT_H5AD)

print("\nStep 8.5 completed successfully.")
