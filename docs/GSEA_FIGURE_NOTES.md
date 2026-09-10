# GSEA Figure Organization

Figure 6 uses the five Hallmark pathways meeting FDR < 0.05:
1. Interferon Alpha Response — NES 1.882, FDR 0
2. Interferon Gamma Response — NES 1.834, FDR 0
3. Allograft Rejection — NES 1.614, FDR 0.007153
4. Oxidative Phosphorylation — NES 1.565, FDR 0.011705
5. Myc Targets V1 — NES 1.481, FDR 0.03512

The supplied one-page GSEA enrichment plots are retained individually in:
`figures/final/supplementary/GSEA_individual_reports/`

The remaining supplied pathway reports did not meet FDR < 0.05 and are retained there as supplementary analysis outputs rather than being presented as significant findings.

The GSEApy log also reported duplicated ranking statistics for 38.66% of genes. GSEA completed successfully, but this ranking-tie issue should be disclosed as a methodological limitation when discussing the enrichment analysis.
