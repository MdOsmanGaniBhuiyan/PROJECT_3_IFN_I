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
# 2. Load QC-filtered AnnData
# --------------------------------------------------

input_file = results_dir / "adata_qc_filtered.h5ad"

print(f"Loading: {input_file}")

adata = sc.read_h5ad(input_file)

print(
    f"Loaded dataset: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)


# --------------------------------------------------
# 3. Save raw counts
# --------------------------------------------------
# Keep the original count matrix before normalization.
# This will be useful for downstream analysis.

adata.layers["counts"] = adata.X.copy()


# --------------------------------------------------
# 4. Normalize total counts
# --------------------------------------------------
# Each cell is scaled to a total of 10,000 counts.

print("\nNormalizing counts...")

sc.pp.normalize_total(
    adata,
    target_sum=1e4,
)


# --------------------------------------------------
# 5. Log-transform
# --------------------------------------------------
# log1p(x) = log(1 + x)

print("Applying log1p transformation...")

sc.pp.log1p(adata)


# --------------------------------------------------
# 6. Identify highly variable genes
# --------------------------------------------------
# Select the top 2,500 variable genes.

print("Selecting 2,500 highly variable genes...")

sc.pp.highly_variable_genes(
    adata,
    n_top_genes=2500,
    flavor="seurat",
)


# --------------------------------------------------
# 7. Report HVG results
# --------------------------------------------------

print(
    f"\nHighly variable genes selected: "
    f"{adata.var['highly_variable'].sum():,}"
)


# --------------------------------------------------
# 8. Save HVG plot
# --------------------------------------------------

sc.pl.highly_variable_genes(
    adata,
    show=False,
)

plt.savefig(
    figures_dir / "highly_variable_genes.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print(
    f"Saved HVG plot: "
    f"{figures_dir / 'highly_variable_genes.png'}"
)


# --------------------------------------------------
# 9. Save normalized AnnData
# --------------------------------------------------

output_file = results_dir / "adata_normalized_hvg.h5ad"

adata.write(output_file)

print(
    f"\nSaved normalized/HVG AnnData: "
    f"{output_file}"
)
