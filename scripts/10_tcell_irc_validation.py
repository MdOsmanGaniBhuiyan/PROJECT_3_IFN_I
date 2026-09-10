import scanpy as sc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# INPUT / OUTPUT
# ============================================================

INPUT = "results/adata_irc_scored.h5ad"

OUTPUT = "results/adata_tcell_irc.h5ad"

SUMMARY_OUTPUT = "results/tcell_irc_summary.csv"

UMAP_OUTPUT = "figures/umap_tcell_irc_status.png"

SCORE_OUTPUT = "figures/tcell_irc_score_by_subtype.png"


# ============================================================
# 1. LOAD DATA
# ============================================================

print(f"Loading: {INPUT}")

adata = sc.read_h5ad(INPUT)

print(
    f"Dataset: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)


# ============================================================
# 2. DEFINE T-CELL POPULATIONS
# ============================================================

tcell_types = [
    "Naive/resting T cell",
    "Naive/memory T cell",
    "Memory CD4/GZMK T cell",
    "Treg-like/activated CD4 T cell",
    "Cytotoxic T/NK",
    "Cytotoxic NK/T",
]


# ============================================================
# 3. CHECK CELL-TYPE LABELS
# ============================================================

available_types = adata.obs["cell_type"].unique()

print("\nT-cell populations requested:")

for cell_type in tcell_types:
    if cell_type in available_types:
        print(f"  ✓ {cell_type}")
    else:
        print(f"  ✗ {cell_type} NOT FOUND")


# ============================================================
# 4. SUBSET T CELLS
# ============================================================

adata_t = adata[
    adata.obs["cell_type"].isin(tcell_types)
].copy()

print("\n" + "=" * 70)
print("T-CELL SUBSET")
print("=" * 70)

print(
    f"T-cell dataset: "
    f"{adata_t.n_obs:,} cells × {adata_t.n_vars:,} genes"
)


print("\nT-cell subtype counts:")

print(
    adata_t.obs["cell_type"]
    .value_counts()
)


# ============================================================
# 5. IRC SCORE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("T-CELL IRC SCORE")
print("=" * 70)

print(
    adata_t.obs["IRC_score"].describe()
)


# ============================================================
# 6. T-CELL IRC HIGH / LOW
# ============================================================
#
# Important:
# We calculate the cutoff WITHIN T CELLS rather than
# using the global cutoff from all 94,513 cells.
#
# This is more appropriate for the T-cell-focused analysis.
# ============================================================

tcell_cutoff = adata_t.obs["IRC_score"].median()

adata_t.obs["Tcell_IRC_status"] = np.where(
    adata_t.obs["IRC_score"] >= tcell_cutoff,
    "IRC_High",
    "IRC_Low"
)

print(
    f"\nT-cell IRC median cutoff: "
    f"{tcell_cutoff:.6f}"
)

print("\nT-cell IRC status:")

print(
    adata_t.obs["Tcell_IRC_status"]
    .value_counts()
)


# ============================================================
# 7. IRC SCORE BY T-CELL SUBTYPE
# ============================================================

summary = (
    adata_t.obs
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

print("\n" + "=" * 70)
print("IRC SCORE BY T-CELL SUBTYPE")
print("=" * 70)

print(
    summary.to_string()
)


# ============================================================
# 8. SAVE SUMMARY
# ============================================================

summary.to_csv(
    SUMMARY_OUTPUT
)

print(
    f"\nSaved:"
    f"\n{SUMMARY_OUTPUT}"
)


# ============================================================
# 9. IRC HIGH / LOW BY T-CELL SUBTYPE
# ============================================================

status_table = pd.crosstab(
    adata_t.obs["cell_type"],
    adata_t.obs["Tcell_IRC_status"]
)

print("\n" + "=" * 70)
print("IRC HIGH / LOW BY T-CELL SUBTYPE")
print("=" * 70)

print(
    status_table.to_string()
)


status_table.to_csv(
    "results/tcell_irc_high_low_by_subtype.csv"
)


# ============================================================
# 10. CREATE T-CELL UMAP
# ============================================================

print("\nCreating T-cell IRC UMAP...")

sc.pl.umap(
    adata_t,
    color="Tcell_IRC_status",
    frameon=False,
    title="T-cell IFN-I Response Capacity",
    show=False
)

plt.savefig(
    UMAP_OUTPUT,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Saved: {UMAP_OUTPUT}"
)


# ============================================================
# 11. IRC SCORE BY T-CELL SUBTYPE
# ============================================================

print("\nCreating IRC score plot...")

plt.figure(figsize=(12, 7))

adata_t.obs.boxplot(
    column="IRC_score",
    by="cell_type",
    rot=60,
    figsize=(12, 7)
)

plt.suptitle("")

plt.title(
    "IFN-I IRC Score Across T-cell Subtypes"
)

plt.xlabel("T-cell subtype")

plt.ylabel("IRC Score")

plt.tight_layout()

plt.savefig(
    SCORE_OUTPUT,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Saved: {SCORE_OUTPUT}"
)


# ============================================================
# 12. SAVE T-CELL DATASET
# ============================================================

print("\nSaving T-cell IRC dataset...")

adata_t.write_h5ad(
    OUTPUT,
    compression="gzip"
)

print(
    f"Saved:"
    f"\n{OUTPUT}"
)


# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("T-CELL IRC VALIDATION COMPLETE")
print("=" * 70)

print(
    f"T cells: {adata_t.n_obs:,}"
)

print(
    f"Genes: {adata_t.n_vars:,}"
)

print(
    f"IRC cutoff: {tcell_cutoff:.6f}"
)

print("\nOutputs:")

print(
    "  results/adata_tcell_irc.h5ad"
)

print(
    "  results/tcell_irc_summary.csv"
)

print(
    "  results/tcell_irc_high_low_by_subtype.csv"
)

print(
    "  figures/umap_tcell_irc_status.png"
)

print(
    "  figures/tcell_irc_score_by_subtype.png"
)

print(
    "\nReady for IRC_High vs IRC_Low differential expression."
)
