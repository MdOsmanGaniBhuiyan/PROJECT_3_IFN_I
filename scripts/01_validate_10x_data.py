from pathlib import Path
import scanpy as sc

data_dir = Path("data")

sample_dirs = sorted(
    [
        p
        for p in data_dir.iterdir()
        if p.is_dir() and (p / "matrix.mtx.gz").exists()
    ]
)

print(f"Found {len(sample_dirs)} samples:")
print([p.name for p in sample_dirs])
print()

for sample_path in sample_dirs:
    sample_id = sample_path.name

    adata = sc.read_10x_mtx(
        path=sample_path,
        var_names="gene_symbols",
        cache=False,
    )

    print(
        f"{sample_id}: "
        f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
    )
