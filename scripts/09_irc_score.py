import scanpy as sc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# INPUT / OUTPUT
# ============================================================

INPUT = "results/adata_annotated_full.h5ad"

OUTPUT = "results/adata_irc_scored.h5ad"

IRC_UMAP = "figures/umap_irc_score.png"

IRC_STATUS_UMAP = "figures/umap_irc_status.png"

IRC_BY_CELLTYPE = "figures/irc_score_by_cell_type.png"

IRC_SUMMARY = "results/irc_summary_by_cell_type.csv"


# ============================================================
# 1. LOAD ANNOTATED FULL-GENE DATA
# ============================================================

print(f"Loading: {INPUT}")

adata = sc.read_h5ad(INPUT)

print(
    f"Dataset: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)


# ============================================================
# 2. DEFINE IFN-I RESPONSE CAPACITY / ISP GENES
# ============================================================

irc_genes = [
    "BST2",
    "EIF2AK2",
    "ISG15",
    "MX1",
    "IFIT3",
    "IRF7",
]


# ============================================================
# 3. CHECK GENE AVAILABILITY
# ============================================================

present_genes = [
    gene for gene in irc_genes
    if gene in adata.var_names
]

missing_genes = [
    gene for gene in irc_genes
    if gene not in adata.var_names
]

print("\n" + "=" * 70)
print("IFN-I ISP GENE CHECK")
print("=" * 70)

print("\nRequested genes:")
print(irc_genes)

print("\nPresent:")
print(present_genes)

print("\nMissing:")
print(missing_genes)


if len(present_genes) == 0:
    raise ValueError(
        "None of the IRC genes were found in the dataset."
    )


if missing_genes:
    print(
        "\nWARNING:"
        " Some ISP genes are missing."
        "\nThe IRC score will use only the genes that are present."
    )


# ============================================================
# 4. CHECK WHETHER DATA ARE LOG-NORMALIZED
# ============================================================

print("\nChecking expression values...")

print(
    f"Expression minimum: {adata.X.min():.4f}"
)

print(
    f"Expression maximum: {adata.X.max():.4f}"
)


# ============================================================
# 5. CALCULATE IRC SCORE
# ============================================================

print("\nCalculating IFN-I IRC score...")

sc.tl.score_genes(
    adata,
    gene_list=present_genes,
    score_name="IRC_score",
    use_raw=False,
    random_state=42
)


print("\nIRC score calculated.")

print(
    adata.obs["IRC_score"].describe()
)


# ============================================================
# 6. CLASSIFY IRC HIGH / LOW
# ============================================================
#
# We use the median IRC score as the cutoff.
#
# IRC_score >= median  -> IRC_High
# IRC_score < median   -> IRC_Low
#
# This produces approximately balanced groups and is
# reproducible across the dataset.
# ============================================================

irc_cutoff = adata.obs["IRC_score"].median()

adata.obs["IRC_status"] = np.where(
    adata.obs["IRC_score"] >= irc_cutoff,
    "IRC_High",
    "IRC_Low"
)

print("\n" + "=" * 70)
print("IRC CLASSIFICATION")
print("=" * 70)

print(
    f"IRC median cutoff: {irc_cutoff:.6f}"
)

print("\nIRC status counts:")

print(
    adata.obs["IRC_status"]
    .value_counts()
)


# ============================================================
# 7. SAVE IRC SCORE PER CELL
# ============================================================

irc_cell_table = adata.obs[
    [
        "leiden",
        "cell_type",
        "annotation_confidence",
        "IRC_score",
        "IRC_status",
    ]
].copy()

irc_cell_table.to_csv(
    "results/irc_scores_per_cell.csv"
)

print(
    "\nSaved per-cell IRC scores:"
    "\nresults/irc_scores_per_cell.csv"
)


# ============================================================
# 8. UMAP — CONTINUOUS IRC SCORE
# ============================================================

print("\nCreating IRC score UMAP...")

sc.pl.umap(
    adata,
    color="IRC_score",
    cmap="viridis",
    frameon=False,
    title="IFN-I Response Capacity (IRC) Score",
    show=False
)

plt.savefig(
    IRC_UMAP,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Saved: {IRC_UMAP}"
)


# ============================================================
# 9. UMAP — IRC HIGH / LOW
# ============================================================

print("\nCreating IRC status UMAP...")

sc.pl.umap(
    adata,
    color="IRC_status",
    frameon=False,
    title="IFN-I Response Capacity",
    show=False
)

plt.savefig(
    IRC_STATUS_UMAP,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Saved: {IRC_STATUS_UMAP}"
)


# ============================================================
# 10. IRC SCORE BY CELL TYPE
# ============================================================

print("\nCalculating IRC statistics by cell type...")

irc_summary = (
    adata.obs
    .groupby("cell_type", observed=True)["IRC_score"]
    .agg(
        [
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max",
        ]
    )
    .sort_values("mean", ascending=False)
)

print("\nIRC score by cell type:")
print(irc_summary.to_string())


# ============================================================
# 11. SAVE IRC SUMMARY
# ============================================================

irc_summary.to_csv(
    IRC_SUMMARY
)

print(
    f"\nSaved:"
    f"\n{IRC_SUMMARY}"
)


# ============================================================
# 12. BOXPLOT — IRC SCORE BY CELL TYPE
# ============================================================

print("\nCreating IRC score boxplot...")

plt.figure(figsize=(14, 8))

adata.obs.boxplot(
    column="IRC_score",
    by="cell_type",
    rot=90,
    figsize=(14, 8)
)

plt.suptitle("")

plt.title(
    "IFN-I Response Capacity Score by Cell Type"
)

plt.xlabel("Cell Type")

plt.ylabel("IRC Score")

plt.tight_layout()

plt.savefig(
    IRC_BY_CELLTYPE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Saved: {IRC_BY_CELLTYPE}"
)


# ============================================================
# 13. SAVE FINAL DATASET
# ============================================================

print("\nSaving IRC-scored dataset...")

adata.write_h5ad(
    OUTPUT,
    compression="gzip"
)

print(
    f"Saved:"
    f"\n{OUTPUT}"
)


# ============================================================
# 14. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 8.6 — IRC SCORING COMPLETE")
print("=" * 70)

print(
    f"Cells: {adata.n_obs:,}"
)

print(
    f"Genes: {adata.n_vars:,}"
)

print(
    f"IRC genes used: {len(present_genes)}"
)

print(
    f"IRC cutoff: {irc_cutoff:.6f}"
)

print("\nOutputs:")

print(
    "  results/adata_irc_scored.h5ad"
)

print(
    "  results/irc_scores_per_cell.csv"
)

print(
    "  results/irc_summary_by_cell_type.csv"
)

print(
    "  figures/umap_irc_score.png"
)

print(
    "  figures/umap_irc_status.png"
)

print(
    "  figures/irc_score_by_cell_type.png"
)

print("\nReady for downstream IRC_High vs IRC_Low analysis.")
