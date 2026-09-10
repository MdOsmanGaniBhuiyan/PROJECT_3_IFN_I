from pathlib import Path

import scanpy as sc
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Define directories
# --------------------------------------------------

results_dir = Path("results")
figures_dir = Path("figures")

results_dir.mkdir(exist_ok=True)
figures_dir.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. Load normalized/HVG AnnData
# --------------------------------------------------

input_file = results_dir / "adata_normalized_hvg.h5ad"

print(f"Loading: {input_file}")

adata = sc.read_h5ad(input_file)

print(
    f"Loaded dataset: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)


# --------------------------------------------------
# 3. Keep only highly variable genes
# --------------------------------------------------

print("\nSubsetting to highly variable genes...")

adata = adata[:, adata.var["highly_variable"]].copy()

print(
    f"Dataset after HVG selection: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)


# --------------------------------------------------
# 4. Scale the data
# --------------------------------------------------

print("\nScaling data...")

sc.pp.scale(
    adata,
    max_value=10,
)


# --------------------------------------------------
# 5. Principal Component Analysis
# --------------------------------------------------

print("Running PCA...")

sc.tl.pca(
    adata,
    n_comps=30,
    svd_solver="arpack",
)


print("PCA completed.")


# --------------------------------------------------
# 6. Save PCA variance plot
# --------------------------------------------------

sc.pl.pca_variance_ratio(
    adata,
    n_pcs=30,
    log=True,
    show=False,
)

plt.savefig(
    figures_dir / "pca_variance_ratio.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print(
    f"Saved PCA variance plot: "
    f"{figures_dir / 'pca_variance_ratio.png'}"
)


# --------------------------------------------------
# 7. Construct neighborhood graph
# --------------------------------------------------

print("\nCalculating neighborhood graph...")

sc.pp.neighbors(
    adata,
    n_neighbors=20,
    n_pcs=30,
)

print("Neighborhood graph completed.")


# --------------------------------------------------
# 8. UMAP
# --------------------------------------------------

print("Running UMAP...")

sc.tl.umap(
    adata,
    random_state=42,
)

print("UMAP completed.")


# --------------------------------------------------
# 9. Save UMAP plot
# --------------------------------------------------

sc.pl.umap(
    adata,
    color="sample",
    show=False,
)

plt.savefig(
    figures_dir / "umap_by_sample.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print(
    f"Saved UMAP by sample: "
    f"{figures_dir / 'umap_by_sample.png'}"
)


# --------------------------------------------------
# 10. Leiden clustering
# --------------------------------------------------

print("\nRunning Leiden clustering...")

sc.tl.leiden(
    adata,
    resolution=1.0,
    random_state=42,
)

print(
    f"Number of Leiden clusters: "
    f"{adata.obs['leiden'].nunique()}"
)


# --------------------------------------------------
# 11. Save UMAP with clusters
# --------------------------------------------------

sc.pl.umap(
    adata,
    color="leiden",
    legend_loc="on data",
    show=False,
)

plt.savefig(
    figures_dir / "umap_leiden_clusters.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print(
    f"Saved Leiden UMAP: "
    f"{figures_dir / 'umap_leiden_clusters.png'}"
)


# --------------------------------------------------
# 12. Print cluster sizes
# --------------------------------------------------

print("\nCluster sizes:")

print(
    adata.obs["leiden"].value_counts().sort_index()
)


# --------------------------------------------------
# 13. Save final dimensionality-reduction object
# --------------------------------------------------

output_file = results_dir / "adata_pca_umap_leiden.h5ad"

adata.write(output_file)

print(
    f"\nSaved PCA/UMAP/Leiden AnnData: "
    f"{output_file}"
)
