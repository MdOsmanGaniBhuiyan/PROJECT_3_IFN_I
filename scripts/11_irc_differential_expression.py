import scanpy as sc
import pandas as pd
import numpy as np


# ============================================================
# INPUT / OUTPUT
# ============================================================

INPUT = "results/adata_tcell_irc.h5ad"

DE_OUTPUT = "results/irc_high_vs_low_de.csv"

TOP_OUTPUT = "results/irc_high_top50_genes.csv"


# ============================================================
# 1. LOAD T-CELL IRC DATA
# ============================================================

print(f"Loading: {INPUT}")

adata = sc.read_h5ad(INPUT)

print(
    f"Dataset: "
    f"{adata.n_obs:,} cells × {adata.n_vars:,} genes"
)


# ============================================================
# 2. CHECK IRC STATUS
# ============================================================

print("\nIRC status counts:")

print(
    adata.obs["Tcell_IRC_status"]
    .value_counts()
)


# ============================================================
# 3. CHECK CELL-TYPE COMPOSITION
# ============================================================

print("\n" + "=" * 70)
print("T-CELL SUBTYPE × IRC STATUS")
print("=" * 70)

composition = pd.crosstab(
    adata.obs["cell_type"],
    adata.obs["Tcell_IRC_status"]
)

print(composition.to_string())

composition.to_csv(
    "results/tcell_subtype_by_irc_status.csv"
)


# ============================================================
# 4. RUN WILCOXON DIFFERENTIAL EXPRESSION
# ============================================================

print("\n" + "=" * 70)
print("IRC_HIGH VS IRC_LOW DIFFERENTIAL EXPRESSION")
print("=" * 70)

print("\nRunning Wilcoxon test...")

sc.tl.rank_genes_groups(
    adata,
    groupby="Tcell_IRC_status",
    groups=["IRC_High"],
    reference="IRC_Low",
    method="wilcoxon",
    use_raw=False,
    pts=True,
)


print("\nDifferential expression completed.")


# ============================================================
# 5. EXTRACT RESULTS
# ============================================================

result = adata.uns["rank_genes_groups"]

genes = result["names"]["IRC_High"]

scores = result["scores"]["IRC_High"]

pvals = result["pvals"]["IRC_High"]

pvals_adj = result["pvals_adj"]["IRC_High"]

logfoldchanges = result["logfoldchanges"]["IRC_High"]


de = pd.DataFrame(
    {
        "gene": genes,
        "score": scores,
        "logfoldchange": logfoldchanges,
        "pval": pvals,
        "pval_adj": pvals_adj,
    }
)


# ============================================================
# 6. REMOVE INVALID VALUES
# ============================================================

de = de.replace(
    [np.inf, -np.inf],
    np.nan
)

de = de.dropna(
    subset=["gene", "pval_adj"]
)


# ============================================================
# 7. SORT BY SIGNIFICANCE
# ============================================================

de = de.sort_values(
    "pval_adj",
    ascending=True
)


# ============================================================
# 8. ADD SIGNIFICANCE LABEL
# ============================================================

de["significant"] = (
    (de["pval_adj"] < 0.05)
)


# ============================================================
# 9. SAVE COMPLETE DE TABLE
# ============================================================

de.to_csv(
    DE_OUTPUT,
    index=False
)

print(
    f"\nSaved complete DE results:"
    f"\n{DE_OUTPUT}"
)


# ============================================================
# 10. SHOW TOP 50 IRC-HIGH GENES
# ============================================================

top50 = de.head(50).copy()

print("\n" + "=" * 70)
print("TOP 50 GENES IN IRC-HIGH T CELLS")
print("=" * 70)

print(
    top50[
        [
            "gene",
            "logfoldchange",
            "pval",
            "pval_adj",
        ]
    ].to_string(index=False)
)


top50.to_csv(
    TOP_OUTPUT,
    index=False
)

print(
    f"\nSaved:"
    f"\n{TOP_OUTPUT}"
)


# ============================================================
# 11. SHOW SIGNIFICANT GENE COUNTS
# ============================================================

significant = de[
    de["pval_adj"] < 0.05
]

upregulated = significant[
    significant["logfoldchange"] > 0
]

downregulated = significant[
    significant["logfoldchange"] < 0
]

print("\n" + "=" * 70)
print("DE SUMMARY")
print("=" * 70)

print(
    f"Total tested genes: {len(de):,}"
)

print(
    f"Significant genes (FDR < 0.05): "
    f"{len(significant):,}"
)

print(
    f"Higher in IRC_High: "
    f"{len(upregulated):,}"
)

print(
    f"Higher in IRC_Low: "
    f"{len(downregulated):,}"
)


# ============================================================
# 12. SHOW TOP UPREGULATED GENES
# ============================================================

print("\n" + "=" * 70)
print("TOP IRC-HIGH ENRICHED GENES")
print("=" * 70)

print(
    upregulated
    .sort_values("logfoldchange", ascending=False)
    .head(30)[
        [
            "gene",
            "logfoldchange",
            "pval_adj",
        ]
    ]
    .to_string(index=False)
)


# ============================================================
# 13. SHOW TOP IRC-LOW ENRICHED GENES
# ============================================================

print("\n" + "=" * 70)
print("TOP IRC-LOW ENRICHED GENES")
print("=" * 70)

print(
    downregulated
    .sort_values("logfoldchange", ascending=True)
    .head(30)[
        [
            "gene",
            "logfoldchange",
            "pval_adj",
        ]
    ]
    .to_string(index=False)
)


# ============================================================
# 14. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("STEP 8.7 — DIFFERENTIAL EXPRESSION COMPLETE")
print("=" * 70)

print("\nOutputs:")

print(
    "  results/irc_high_vs_low_de.csv"
)

print(
    "  results/irc_high_top50_genes.csv"
)

print(
    "  results/tcell_subtype_by_irc_status.csv"
)

print(
    "\nNext step: GSEA / pathway enrichment."
)
