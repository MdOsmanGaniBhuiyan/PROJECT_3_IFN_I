from pathlib import Path

import scanpy as sc
import anndata as ad
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Define directories
# --------------------------------------------------

data_dir = Path("data")
results_dir = Path("results")
figures_dir = Path("figures")

results_dir.mkdir(exist_ok=True)
figures_dir.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. Find all 10x sample directories
# --------------------------------------------------

sample_dirs = sorted(
    [
        p
        for p in data_dir.iterdir()
        if p.is_dir() and (p / "matrix.mtx.gz").exists()
    ]
)

print(f"Found {len(sample_dirs)} samples:")
print([p.name for p in sample_dirs])


# --------------------------------------------------
# 3. Load each sample
# --------------------------------------------------

adatas = []

for sample_path in sample_dirs:

    sample_id = sample_path.name

    print(f"Loading {sample_id}...")

    adata_sample = sc.read_10x_mtx(
        path=sample_path,
        var_names="gene_symbols",
        cache=False,
    )

    adata_sample.obs["sample"] = sample_id

    if sample_id.startswith("HD"):
        adata_sample.obs["donor_type"] = "Healthy"
    else:
        adata_sample.obs["donor_type"] = "Patient"

    adatas.append(adata_sample)


# --------------------------------------------------
# 4. Combine samples
# --------------------------------------------------

adata = ad.concat(
    adatas,
    label="sample_batch",
    index_unique="-",
    join="outer",
)

adata.var_names_make_unique()

print()
print(f"Initial dataset: {adata.n_obs:,} cells × {adata.n_vars:,} genes")


# --------------------------------------------------
# 5. Identify QC gene categories
# --------------------------------------------------

adata.var["mt"] = adata.var_names.str.startswith("MT-")

adata.var["ribo"] = adata.var_names.str.startswith(
    ("RPS", "RPL")
)

adata.var["hb"] = adata.var_names.str.contains(
    r"^HB[AB]"
)


# --------------------------------------------------
# 6. Calculate QC metrics
# --------------------------------------------------

sc.pp.calculate_qc_metrics(
    adata,
    qc_vars=["mt", "ribo", "hb"],
    inplace=True,
)


# --------------------------------------------------
# 7. Print QC summary
# --------------------------------------------------

print("\nQC summary:")

print(
    adata.obs[
        [
            "n_genes_by_counts",
            "total_counts",
            "pct_counts_mt",
            "pct_counts_ribo",
            "pct_counts_hb",
        ]
    ].describe()
)


print("\nQC summary by donor type:")

print(
    adata.obs.groupby("donor_type")[
        [
            "n_genes_by_counts",
            "total_counts",
            "pct_counts_mt",
            "pct_counts_ribo",
            "pct_counts_hb",
        ]
    ].median()
)


# --------------------------------------------------
# 8. Save QC violin plots BEFORE filtering
# --------------------------------------------------

sc.pl.violin(
    adata,
    [
        "n_genes_by_counts",
        "total_counts",
        "pct_counts_mt",
        "pct_counts_ribo",
        "pct_counts_hb",
    ],
    groupby="donor_type",
    rotation=45,
    show=False,
)

plt.tight_layout()

plt.savefig(
    figures_dir / "qc_violin_before_filtering.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print(
    f"\nSaved QC plot: "
    f"{figures_dir / 'qc_violin_before_filtering.png'}"
)


# --------------------------------------------------
# 9. Apply mentor-specified filters
# --------------------------------------------------

before_cells = adata.n_obs
before_genes = adata.n_vars

sc.pp.filter_cells(
    adata,
    min_genes=300,
)

sc.pp.filter_genes(
    adata,
    min_cells=5,
)

adata = adata[
    (adata.obs["pct_counts_mt"] < 15)
    & (adata.obs["pct_counts_hb"] < 5)
].copy()


# --------------------------------------------------
# 10. Report filtering result
# --------------------------------------------------

print("\nFiltering result:")

print(f"Cells before filtering: {before_cells:,}")
print(f"Cells after filtering:  {adata.n_obs:,}")

print(f"Genes before filtering: {before_genes:,}")
print(f"Genes after filtering:  {adata.n_vars:,}")


print("\nCells remaining by sample:")

print(
    adata.obs["sample"].value_counts()
)


print("\nCells remaining by donor type:")

print(
    adata.obs["donor_type"].value_counts()
)


# --------------------------------------------------
# 11. Save filtered AnnData
# --------------------------------------------------

output_file = results_dir / "adata_qc_filtered.h5ad"

adata.write(output_file)

print()
print(f"Saved filtered AnnData: {output_file}")

