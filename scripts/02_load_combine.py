from pathlib import Path

import scanpy as sc
import anndata as ad


# --------------------------------------------------
# 1. Define data directory
# --------------------------------------------------

data_dir = Path("data")


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

    adata = sc.read_10x_mtx(
        path=sample_path,
        var_names="gene_symbols",
        cache=False,
    )

    # Add sample identity
    adata.obs["sample"] = sample_id

    # Add donor type
    if sample_id.startswith("HD"):
        adata.obs["donor_type"] = "Healthy"
    else:
        adata.obs["donor_type"] = "Patient"

    adatas.append(adata)


# --------------------------------------------------
# 4. Combine all samples
# --------------------------------------------------

adata = ad.concat(
    adatas,
    label="sample_batch",
    index_unique="-",
    join="outer",
)


# --------------------------------------------------
# 5. Make gene names unique
# --------------------------------------------------

adata.var_names_make_unique()


# --------------------------------------------------
# 6. Report combined dataset
# --------------------------------------------------

print()
print("Combined AnnData:")
print(adata)

print()
print("Cells by donor type:")
print(adata.obs["donor_type"].value_counts())

print()
print("Cells by sample:")
print(adata.obs["sample"].value_counts())
