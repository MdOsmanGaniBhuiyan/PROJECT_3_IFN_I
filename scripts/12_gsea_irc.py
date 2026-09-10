from pathlib import Path
import pandas as pd
import numpy as np
import gseapy as gp


# ============================================================
# STEP 8.8 — GSEA / PATHWAY ENRICHMENT
# IRC_High vs IRC_Low T cells
# ============================================================

results_dir = Path("results")
gsea_dir = results_dir / "gsea"
gsea_dir.mkdir(parents=True, exist_ok=True)

de_file = results_dir / "irc_high_vs_low_de.csv"

print("=" * 70)
print("STEP 8.8 — GSEA / PATHWAY ENRICHMENT")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load DE results
# ------------------------------------------------------------

print(f"\nLoading: {de_file}")

de = pd.read_csv(de_file)

print(f"Loaded DE table: {de.shape[0]:,} genes")

required = ["gene", "score", "logfoldchange", "pval_adj"]
missing = [x for x in required if x not in de.columns]

if missing:
    raise ValueError(
        f"Missing required columns: {missing}\n"
        f"Available columns: {list(de.columns)}"
    )

# ------------------------------------------------------------
# 2. Clean gene names and ranking statistic
# ------------------------------------------------------------

de["gene"] = de["gene"].astype(str).str.upper()

de["score"] = pd.to_numeric(de["score"], errors="coerce")
de = de.replace([np.inf, -np.inf], np.nan)

de = de.dropna(subset=["gene", "score"])
# Remove duplicate genes
de = de.drop_duplicates(subset="gene", keep="first")

# Sort from most IRC_High-associated to most IRC_Low-associated
de = de.sort_values("score", ascending=False)
print(f"Genes available for GSEA ranking: {len(de):,}")

print("\nTop 10 genes in ranking:")
print(
de[["gene", "score", "logfoldchange"]]
    .head(10)
    .to_string(index=False)
)

print("\nBottom 10 genes in ranking:")
print(
    de[["gene", "score", "logfoldchange"]]
    .tail(10)
    .to_string(index=False)
)

# ------------------------------------------------------------
# 3. Save ranked gene list
# ------------------------------------------------------------

ranking = de[["gene", "score"]].copy()
ranking_file = gsea_dir / "irc_high_vs_low_ranked_genes.rnk"

ranking.to_csv(
    ranking_file,
    sep="\t",
    index=False,
    header=False
)

print(f"\nSaved ranked gene list:")
print(ranking_file)

# ------------------------------------------------------------
# 4. Run Hallmark GSEA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RUNNING HALLMARK GSEA")
print("=" * 70)

print(
    "\nUsing MSigDB Hallmark gene sets through GSEApy..."
)

pre_res = gp.prerank(
    rnk=str(ranking_file),
    gene_sets="MSigDB_Hallmark_2020",
    outdir=str(gsea_dir / "hallmark"),
    permutation_num=1000,
    min_size=10,
    max_size=500,
    seed=42,
    verbose=True
)

# ------------------------------------------------------------
# 5. Extract results
# ------------------------------------------------------------

res = pre_res.res2d.copy()

print("\nGSEA completed.")

print("\nAvailable result columns:")
print(list(res.columns))

# Normalize pathway column name
if "Term" in res.columns:
    pathway_col = "Term"
elif "Name" in res.columns:
    pathway_col = "Name"
else:
    pathway_col = res.columns[0]

# ------------------------------------------------------------
# 6. Save complete GSEA results
# ------------------------------------------------------------

gsea_results_file = gsea_dir / "hallmark_gsea_results.csv"

res.to_csv(gsea_results_file, index=False)

print(f"\nSaved complete GSEA results:")
print(gsea_results_file)

# ------------------------------------------------------------
# 7. Display significant pathways
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SIGNIFICANT HALLMARK PATHWAYS")
print("=" * 70)

# GSEApy versions may use different capitalization
fdr_col = None

for candidate in ["FDR q-val", "FDR", "fdr"]:
    if candidate in res.columns:
        fdr_col = candidate
        break

if fdr_col is None:
    raise ValueError(
        f"Could not identify FDR column. "
        f"Available columns: {list(res.columns)}"
    )

res[fdr_col] = pd.to_numeric(
    res[fdr_col],
    errors="coerce"
)

significant = res[
    res[fdr_col] < 0.05
].copy()

significant = significant.sort_values(
    fdr_col,
    ascending=True
)

print(
    f"\nSignificant pathways (FDR < 0.05): "
    f"{len(significant)}"
)

if len(significant) > 0:
    print(
        significant[
            [pathway_col, "NES", "NOM p-val", fdr_col]
        ].to_string(index=False)
    )
else:
    print("No pathways reached FDR < 0.05.")

# ------------------------------------------------------------
# 8. IRC_High enriched pathways
# ------------------------------------------------------------

high = significant[
    significant["NES"] > 0
].copy()

high = high.sort_values(
    "NES",
    ascending=False
)

high_file = gsea_dir / "irc_high_enriched_hallmark.csv"

high.to_csv(high_file, index=False)

print("\n" + "=" * 70)
print("IRC-HIGH ENRICHED PATHWAYS")
print("=" * 70)

if len(high) > 0:
    print(
        high[
            [pathway_col, "NES", "NOM p-val", fdr_col]
        ].to_string(index=False)
    )
else:
    print("No significant pathways enriched in IRC_High.")

# ------------------------------------------------------------
# 9. IRC_Low enriched pathways
# ------------------------------------------------------------

low = significant[
    significant["NES"] < 0
].copy()

low = low.sort_values(
    "NES",
    ascending=True
)

low_file = gsea_dir / "irc_low_enriched_hallmark.csv"

low.to_csv(low_file, index=False)

print("\n" + "=" * 70)
print("IRC-LOW ENRICHED PATHWAYS")
print("=" * 70)

if len(low) > 0:
    print(
        low[
            [pathway_col, "NES", "NOM p-val", fdr_col]
        ].to_string(index=False)
    )
else:
    print("No significant pathways enriched in IRC_Low.")

# ------------------------------------------------------------
# 10. Summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 8.8 — GSEA COMPLETE")
print("=" * 70)

print("\nOutputs:")

print(f"  {ranking_file}")
print(f"  {gsea_results_file}")
print(f"  {high_file}")
print(f"  {low_file}")

print(
    "\nGSEA interpretation:"
)

print(
    "  NES > 0  → pathway enriched toward IRC_High"
)

print(
    "  NES < 0  → pathway enriched toward IRC_Low"
)

print(
    "  FDR < 0.05 → statistically significant pathway"
)
