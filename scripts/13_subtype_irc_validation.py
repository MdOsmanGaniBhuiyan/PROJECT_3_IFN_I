from pathlib import Path
import pandas as pd
import numpy as np
import scanpy as sc


# ============================================================
# STEP 8.9 — SUBTYPE-AWARE IRC VALIDATION
# IRC_High vs IRC_Low within each T-cell subtype
# ============================================================

results_dir = Path("results")
output_file = results_dir / "subtype_irc_de_summary.csv"
all_de_file = results_dir / "subtype_irc_de_all_genes.csv"

input_file = results_dir / "adata_tcell_irc.h5ad"

print("=" * 70)
print("STEP 8.9 — SUBTYPE-AWARE IRC VALIDATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load data
# ------------------------------------------------------------

print(f"\nLoading: {input_file}")

adata = sc.read_h5ad(input_file)

print(
    f"Dataset: {adata.n_obs:,} cells × "
    f"{adata.n_vars:,} genes"
)

# ------------------------------------------------------------
# 2. Check required columns
# ------------------------------------------------------------

required_columns = [
    "cell_type",
    "Tcell_IRC_status"
]

missing = [
    col for col in required_columns
    if col not in adata.obs.columns
]

if missing:
    raise ValueError(
        f"Missing required columns: {missing}"
    )

# ------------------------------------------------------------
# 3. Define subtypes
# ------------------------------------------------------------

subtypes = [
    "Naive/resting T cell",
    "Naive/memory T cell",
    "Memory CD4/GZMK T cell",
    "Treg-like/activated CD4 T cell",
    "Cytotoxic T/NK",
    "Cytotoxic NK/T"
]

# ------------------------------------------------------------
# 4. Display subtype counts
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SUBTYPE COUNTS")
print("=" * 70)

counts = pd.crosstab(
    adata.obs["cell_type"],
    adata.obs["Tcell_IRC_status"]
)

print(counts.loc[
    [x for x in subtypes if x in counts.index]
].to_string())

# ------------------------------------------------------------
# 5. IRC genes
# ------------------------------------------------------------

irc_genes = [
    "BST2",
    "EIF2AK2",
    "ISG15",
    "MX1",
    "IFIT3",
    "IRF7"
]

available_irc = [
    g for g in irc_genes
    if g in adata.var_names
]

print("\nIRC genes available:")
print(", ".join(available_irc))

# ------------------------------------------------------------
# 6. Run subtype-specific DE
# ------------------------------------------------------------

all_results = []
summary_results = []

for subtype in subtypes:

    print("\n" + "=" * 70)
    print(f"SUBTYPE: {subtype}")
    print("=" * 70)

    sub = adata[
        adata.obs["cell_type"] == subtype
    ].copy()

    print(f"Cells: {sub.n_obs:,}")

    status_counts = (
        sub.obs["Tcell_IRC_status"]
        .value_counts()
    )

    high_n = int(status_counts.get("IRC_High", 0))
    low_n = int(status_counts.get("IRC_Low", 0))

    print(f"IRC_High: {high_n:,}")
    print(f"IRC_Low : {low_n:,}")

    # Need both groups
    if high_n < 10 or low_n < 10:
        print("Skipping: insufficient cells in one group.")
        continue

    # --------------------------------------------------------
    # Run Wilcoxon
    # --------------------------------------------------------

    print("Running Wilcoxon DE...")

    sc.tl.rank_genes_groups(
        sub,
        groupby="Tcell_IRC_status",
        groups=["IRC_High"],
        reference="IRC_Low",
        method="wilcoxon",
        use_raw=False,
        pts=True
    )

    # --------------------------------------------------------
    # Extract results
    # --------------------------------------------------------

    result = sc.get.rank_genes_groups_df(
        sub,
        group="IRC_High"
    )

    result = result.rename(
        columns={
            "names": "gene",
            "scores": "score",
            "logfoldchanges": "logfoldchange",
            "pvals": "pval",
            "pvals_adj": "pval_adj"
        }
    )

    result["subtype"] = subtype

    result = result.replace(
        [np.inf, -np.inf],
        np.nan
    )

    result = result.dropna(
        subset=["gene", "score"]
    )

    all_results.append(result)

    # --------------------------------------------------------
    # IRC gene results
    # --------------------------------------------------------

    irc_result = result[
        result["gene"].isin(available_irc)
    ].copy()

    irc_result = irc_result.sort_values(
        "score",
        ascending=False
    )

    print("\nIRC genes in this subtype:")

    if len(irc_result) > 0:
        print(
            irc_result[
                [
                    "gene",
                    "score",
                    "logfoldchange",
                    "pval_adj"
                ]
            ].to_string(index=False)
        )
    else:
        print("No IRC genes found.")

    # --------------------------------------------------------
    # Top 20 High genes
    # --------------------------------------------------------

    high = result[
        result["logfoldchange"] > 0
    ].sort_values(
        "pval_adj",
        ascending=True
    )

    print("\nTop IRC_High genes:")

    print(
        high[
            [
                "gene",
                "logfoldchange",
                "pval_adj"
            ]
        ].head(20).to_string(index=False)
    )

    # --------------------------------------------------------
    # Top 20 Low genes
    # --------------------------------------------------------

    low = result[
        result["logfoldchange"] < 0
    ].sort_values(
        "pval_adj",
        ascending=True
    )

    print("\nTop IRC_Low genes:")

    print(
        low[
            [
                "gene",
                "logfoldchange",
                "pval_adj"
            ]
        ].head(20).to_string(index=False)
    )

    # --------------------------------------------------------
    # Summary of significant genes
    # --------------------------------------------------------

    significant = result[
        result["pval_adj"] < 0.05
    ]

    high_sig = significant[
        significant["logfoldchange"] > 0
    ]

    low_sig = significant[
        significant["logfoldchange"] < 0
    ]

    # Count significant IRC genes
    irc_sig = irc_result[
        irc_result["pval_adj"] < 0.05
    ]

    irc_high_sig = irc_sig[
        irc_sig["logfoldchange"] > 0
    ]

    summary_results.append({
        "subtype": subtype,
        "IRC_High_cells": high_n,
        "IRC_Low_cells": low_n,
        "significant_genes": len(significant),
        "higher_in_IRC_High": len(high_sig),
        "higher_in_IRC_Low": len(low_sig),
        "significant_IRC_genes": len(irc_sig),
        "IRC_genes_higher_in_High": len(irc_high_sig)
    })

# ------------------------------------------------------------
# 7. Save complete results
# ------------------------------------------------------------

if not all_results:
    raise RuntimeError(
        "No subtype had enough cells for DE."
    )

all_de = pd.concat(
    all_results,
    ignore_index=True
)

all_de.to_csv(
    all_de_file,
    index=False
)

summary = pd.DataFrame(summary_results)

summary.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------------------
# 8. Final summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SUBTYPE-AWARE DE SUMMARY")
print("=" * 70)

print(
    summary.to_string(index=False)
)

print("\nSaved:")
print(f"  {all_de_file}")
print(f"  {output_file}")

print("\n" + "=" * 70)
print("STEP 8.9 — SUBTYPE-AWARE VALIDATION COMPLETE")
print("=" * 70)
