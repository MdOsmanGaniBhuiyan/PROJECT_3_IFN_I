import scanpy as sc
import matplotlib.pyplot as plt

INPUT = "results/adata_pca_umap_leiden.h5ad"
OUTPUT = "figures/marker_dotplot.png"

print(f"Loading: {INPUT}")
adata = sc.read_h5ad(INPUT)

print(f"Dataset: {adata.n_obs:,} cells × {adata.n_vars:,} genes")

marker_genes = {
    "T_cell": [
        "CD3D", "CD3E", "TRBC1", "IL7R", "LTB", "CCR7"
    ],
    "NK_cytotoxic": [
        "NKG7", "GNLY", "PRF1", "GZMB", "GZMH", "KLRD1"
    ],
    "B_cell": [
        "MS4A1", "CD79A", "CD74", "HLA-DRA", "CD37", "CD79B"
    ],
    "Myeloid": [
        "LYZ", "LST1", "S100A8", "S100A9", "CTSS", "FCGR3A"
    ],
    "DC_pDC": [
        "FCER1A", "CLEC10A", "CLEC4C", "TCF4", "IL3RA"
    ],
    "Platelet": [
        "PPBP", "PF4", "GP9", "ITGA2B", "GP1BB"
    ],
    "Cycling": [
        "MKI67", "TOP2A", "CENPF", "RRM2"
    ],
    "IFN_I": [
        "BST2", "EIF2AK2", "ISG15", "MX1", "IFIT3", "IRF7"
    ],
}

# Keep only genes present in the dataset
present_genes = []

for group, genes in marker_genes.items():
    present = [g for g in genes if g in adata.var_names]
    present_genes.extend(present)

    missing = [g for g in genes if g not in adata.var_names]

    print(f"\n{group}")
    print("Present:", present)

    if missing:
        print("Missing:", missing)

# Remove duplicates while preserving order
present_genes = list(dict.fromkeys(present_genes))

print("\nTotal marker genes present:", len(present_genes))

sc.pl.dotplot(
    adata,
    var_names=present_genes,
    groupby="leiden",
    standard_scale="var",
    dendrogram=False,
    show=False
)

plt.savefig(
    OUTPUT,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"\nSaved: {OUTPUT}")
