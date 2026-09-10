import scanpy as sc
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# INPUT / OUTPUT
# ============================================================

FULL_GENE_INPUT = "results/adata_normalized_hvg.h5ad"
CLUSTER_INPUT = "results/adata_pca_umap_leiden.h5ad"

ANNOTATED_OUTPUT = "results/adata_annotated_full.h5ad"
ANNOTATION_TABLE = "results/cluster_annotations.csv"
UMAP_OUTPUT = "figures/umap_annotated_cell_types.png"


# ============================================================
# 1. LOAD FULL-GENE NORMALIZED DATA
# ============================================================

print(f"Loading full-gene data: {FULL_GENE_INPUT}")

adata = sc.read_h5ad(FULL_GENE_INPUT)

print(
    f"Full-gene dataset: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)


# ============================================================
# 2. LOAD LEIDEN / UMAP DATA
# ============================================================

print(f"\nLoading clustering data: {CLUSTER_INPUT}")

adata_cluster = sc.read_h5ad(CLUSTER_INPUT)

print(
    f"Clustering dataset: "
    f"{adata_cluster.n_obs:,} cells × {adata_cluster.n_vars:,} genes"
)


# ============================================================
# 3. CHECK CELL IDs
# ============================================================

if not adata.obs_names.equals(adata_cluster.obs_names):

    print("\nCell order differs between datasets.")
    print("Aligning clustering information to full-gene dataset...")

    if not set(adata.obs_names).issubset(set(adata_cluster.obs_names)):
        raise ValueError(
            "The full-gene dataset contains cells that are "
            "missing from the clustering dataset."
        )

    adata_cluster = adata_cluster[adata.obs_names].copy()

else:
    print("\nCell IDs match.")


# ============================================================
# 4. TRANSFER LEIDEN CLUSTERS
# ============================================================

adata.obs["leiden"] = adata_cluster.obs["leiden"].astype(str)

print("\nLeiden clusters transferred successfully.")

print("\nCluster counts:")
print(adata.obs["leiden"].value_counts().sort_index())


# ============================================================
# 5. TRANSFER UMAP COORDINATES
# ============================================================

if "X_umap" not in adata_cluster.obsm:

    raise ValueError(
        "X_umap was not found in the clustering dataset."
    )

adata.obsm["X_umap"] = adata_cluster.obsm["X_umap"].copy()

print("\nUMAP coordinates transferred successfully.")


# ============================================================
# 6. EVIDENCE-BASED CLUSTER ANNOTATIONS
# ============================================================

cluster_annotations = {

    # --------------------------------------------------------
    # T-cell populations
    # --------------------------------------------------------

    "0": "Naive/resting T cell",

    "16": "Naive/memory T cell",

    "20": "Treg-like/activated CD4 T cell",

    "22": "Memory CD4/GZMK T cell",


    # --------------------------------------------------------
    # Myeloid / APC populations
    # --------------------------------------------------------

    "1": "Myeloid",

    "2": "Myeloid/APC",

    "3": "Myeloid/APC",

    "4": "Myeloid",

    "5": "Myeloid/APC",

    "6": "Myeloid/APC",

    "8": "Myeloid/T-cell mixed",

    "9": "Activated myeloid/APC",

    "10": "Activated myeloid/APC",

    "11": "Monocyte/myeloid",

    "12": "Activated myeloid/APC",

    "14": "Myeloid/APC",

    "21": "Activated/inflammatory myeloid",

    "31": "IFN-stimulated myeloid",


    # --------------------------------------------------------
    # Cytotoxic T / NK populations
    # --------------------------------------------------------

    "13": "Cytotoxic T/NK",

    "15": "Cytotoxic NK/T",

    "25": "NK cell",


    # --------------------------------------------------------
    # B-cell populations
    # --------------------------------------------------------

    "18": "B cell",

    "19": "B cell",

    "23": "B cell",

    "26": "B cell",


    # --------------------------------------------------------
    # Dendritic cells
    # --------------------------------------------------------

    "24": "Dendritic/APC",

    "28": "pDC-like",


    # --------------------------------------------------------
    # Platelet
    # --------------------------------------------------------

    "27": "Platelet",


    # --------------------------------------------------------
    # Cycling
    # --------------------------------------------------------

    "29": "Cycling/proliferating",


    # --------------------------------------------------------
    # Uncertain populations
    # --------------------------------------------------------

    "7": "Mixed/uncertain",

    "17": "Unclear/rare",

    "30": "Unclear/rare",
}


# ============================================================
# 7. CHECK THAT ALL CLUSTERS HAVE AN ANNOTATION
# ============================================================

clusters = sorted(adata.obs["leiden"].unique(), key=lambda x: int(x))

missing_annotations = [
    cluster
    for cluster in clusters
    if cluster not in cluster_annotations
]

if missing_annotations:

    raise ValueError(
        f"Missing annotations for clusters: {missing_annotations}"
    )

print("\nAll Leiden clusters have annotations.")


# ============================================================
# 8. ADD CELL-TYPE ANNOTATION
# ============================================================

adata.obs["cell_type"] = (
    adata.obs["leiden"]
    .map(cluster_annotations)
)


# ============================================================
# 9. ADD ANNOTATION CONFIDENCE
# ============================================================

confidence = {

    "0": "High",
    "1": "High",
    "2": "High",
    "3": "High",
    "4": "High",
    "5": "High",
    "6": "High",
    "7": "Low",
    "8": "Low",
    "9": "Moderate",
    "10": "Moderate",
    "11": "High",
    "12": "Moderate",
    "13": "High",
    "14": "Moderate",
    "15": "High",
    "16": "High",
    "17": "Low",
    "18": "Moderate",
    "19": "High",
    "20": "Moderate",
    "21": "Moderate",
    "22": "High",
    "23": "High",
    "24": "Moderate",
    "25": "High",
    "26": "High",
    "27": "High",
    "28": "Moderate",
    "29": "High",
    "30": "Low",
    "31": "Moderate",
}

adata.obs["annotation_confidence"] = (
    adata.obs["leiden"]
    .map(confidence)
)


# ============================================================
# 10. PRINT ANNOTATION SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL CLUSTER ANNOTATION")
print("=" * 70)

annotation_summary = (
    adata.obs[["leiden", "cell_type", "annotation_confidence"]]
    .drop_duplicates()
    .sort_values(
        "leiden",
        key=lambda x: x.astype(int)
    )
)

print(annotation_summary.to_string(index=False))


# ============================================================
# 11. SAVE ANNOTATION TABLE
# ============================================================

annotation_summary.to_csv(
    ANNOTATION_TABLE,
    index=False
)

print(f"\nSaved annotation table:")
print(ANNOTATION_TABLE)


# ============================================================
# 12. MAKE ANNOTATED UMAP
# ============================================================

print("\nCreating annotated UMAP...")

sc.pl.umap(
    adata,
    color="cell_type",
    legend_loc="right margin",
    frameon=False,
    title="Annotated Cell Types",
    show=False
)

plt.savefig(
    UMAP_OUTPUT,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Saved annotated UMAP:")
print(UMAP_OUTPUT)


# ============================================================
# 13. SAVE FULL-GENE ANNOTATED DATASET
# ============================================================

print("\nSaving full-gene annotated AnnData...")

adata.write_h5ad(
    ANNOTATED_OUTPUT,
    compression="gzip"
)

print(f"Saved:")
print(ANNOTATED_OUTPUT)


# ============================================================
# 14. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 8 ANNOTATION COMPLETE")
print("=" * 70)

print(
    f"Cells: {adata.n_obs:,}"
)

print(
    f"Genes: {adata.n_vars:,}"
)

print(
    f"Clusters: {adata.obs['leiden'].nunique()}"
)

print(
    f"Cell types: {adata.obs['cell_type'].nunique()}"
)

print("\nOutputs:")
print(f"  {ANNOTATED_OUTPUT}")
print(f"  {ANNOTATION_TABLE}")
print(f"  {UMAP_OUTPUT}")

print("\nReady for Step 8.6: IFN-I IRC scoring.")
