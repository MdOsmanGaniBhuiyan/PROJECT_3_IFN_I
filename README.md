# PROJECT 3 — Type I Interferon Immunotherapy Response

## Single-Cell RNA-seq Analysis

This repository contains the computational workflow, analysis scripts, results, figures, documentation, and final report for **Project 3: Type I Interferon Immunotherapy Response**.

The project analyzes baseline peripheral blood mononuclear cell (PBMC) single-cell RNA-seq data to investigate immune-cell composition and transcriptional signatures associated with **Type I interferon (IFN-I) responsiveness**, with particular focus on T cells.

---

## Project Overview

Type I interferon signaling plays an important role in regulating immune responses and may influence the outcome of cancer immunotherapy.

The biological motivation for this project comes from the study:

**Pre-encoded responsiveness to type I interferon in the peripheral immune system defines outcome of PD1 blockade therapy**

The study reported that pre-existing IFN-I responsiveness in peripheral immune cells, particularly effector T cells, was associated with the outcome of PD-1 blockade therapy.

This project uses single-cell RNA-seq data to characterize peripheral immune-cell populations and investigate a transcriptomic proxy of IFN-I responsiveness.

---

## Dataset

The analysis uses baseline PBMC single-cell RNA-seq data from **10 samples**:

| Group           | Samples            | Number |
| --------------- | ------------------ | -----: |
| Healthy donors  | HD1, HD2           |      2 |
| Cancer patients | P1–P8              |      8 |
| **Total**       | **HD1–HD2, P1–P8** | **10** |

### Public dataset

* **GEO accession:** GSE199994
* **Publication:** Nature Immunology, 2022
* **Study:** *Pre-encoded responsiveness to type I interferon in the peripheral immune system defines outcome of PD1 blockade therapy*

---

# Analysis Workflow

The project was implemented as a sequential Python/Scanpy workflow.

```text
10x Genomics input data
        │
        ▼
01. Validate 10x data
        │
        ▼
02. Load and combine samples
        │
        ▼
03. Quality control and filtering
        │
        ▼
04. Normalization + HVG selection
        │
        ▼
05. PCA + neighbors + UMAP + Leiden
        │
        ▼
06. Marker-gene analysis
        │
        ├── 06b. Full-gene marker analysis
        │
        ▼
07. Marker visualization
        │
        ▼
08. Cell-type annotation
        │
        ▼
09. IFN-I response scoring
        │
        ▼
10. T-cell-specific IRC analysis
        │
        ▼
11. IRC differential expression
        │
        ▼
12. GSEA
        │
        ▼
13. T-cell subtype IRC validation
```

---

# Analysis Scripts

## 01 — Validate 10x Genomics Data

**Script:** `scripts/01_validate_10x_data.py`

Validates the expected 10x Genomics input structure.

The script checks the sample directories and verifies that the required matrix files are available before downstream analysis.

---

## 02 — Load and Combine Samples

**Script:** `scripts/02_load_combine.py`

Loads the individual 10x Genomics datasets and combines the samples into a single AnnData object.

Sample-level metadata include:

* Sample identifier
* Healthy/Patient donor category
* Sample batch identifier

Healthy donor samples were identified from sample names beginning with `HD`; the remaining samples were classified as patients.

---

## 03 — Quality Control and Filtering

**Script:** `scripts/03_qc_filter.py`

Quality-control metrics were calculated for:

* Number of genes detected per cell
* Total counts per cell
* Mitochondrial gene percentage
* Ribosomal gene percentage
* Hemoglobin gene percentage

### Filtering criteria

| Metric                 | Threshold |
| ---------------------- | --------: |
| Minimum genes per cell |       300 |
| Minimum cells per gene |         5 |
| Mitochondrial counts   |      <15% |
| Hemoglobin counts      |       <5% |

Ribosomal percentage was calculated and reported but was **not used as a filtering criterion**.

### Dataset after QC

After filtering, the dataset contained:

**94,513 cells × 31,120 genes**

---

# 04 — Normalization and Highly Variable Genes

**Script:** `scripts/04_normalization_hvg.py`

The following steps were performed:

1. Raw counts were stored in an AnnData layer.
2. Counts were normalized to a total of 10,000 counts per cell.
3. A `log1p` transformation was applied.
4. The top **2,500 highly variable genes (HVGs)** were selected.

The Seurat flavor was used for HVG selection.

### Result

The normalized dataset contained:

**94,513 cells × 31,120 genes**

with:

**2,500 highly variable genes selected for downstream dimensionality reduction and clustering.**

---

# 05 — PCA, UMAP and Leiden Clustering

**Script:** `scripts/05_pca_umap_clustering.py`

The workflow performed:

* Scaling
* Principal component analysis (PCA)
* Neighborhood graph construction
* UMAP
* Leiden clustering

### Main parameters

| Parameter                   | Value |
| --------------------------- | ----: |
| Highly variable genes       | 2,500 |
| PCA components              |    30 |
| Number of neighbors         |    20 |
| Number of PCs for neighbors |    30 |
| UMAP random seed            |    42 |
| Leiden resolution           |   1.0 |
| Leiden random seed          |    42 |

### Clustering result

The analysis identified:

**32 Leiden clusters (clusters 0–31)**

Leiden cluster numbers do **not** directly represent biological cell types. Cell identities were determined using marker-gene analysis and biological interpretation.

---

# 06 — Marker Gene Analysis

**Script:** `scripts/06_marker_genes.py`

Wilcoxon differential expression analysis was used to identify genes enriched in individual Leiden clusters.

The analysis generated complete marker-gene results as well as top marker-gene tables for downstream interpretation.

---

# 06b — Full-Gene Marker Analysis

**Script:** `scripts/06b_full_gene_markers.py`

Marker analysis was additionally performed using the full gene set rather than only the highly variable genes.

This provided a broader basis for cell-type annotation and marker interpretation.

---

# 07 — Marker Visualization

**Script:** `scripts/07_marker_dotplot.py`

Marker expression was visualized using dot plots for biologically relevant marker groups.

Marker groups included:

* T cells
* NK cells
* B cells
* Myeloid cells
* Dendritic cells / pDCs
* Platelets
* Cycling cells
* IFN-I-associated genes

---

# 08 — Cell-Type Annotation

**Script:** `scripts/08_annotate_cells.py`

Leiden clusters were assigned cell-type labels based on marker-gene expression.

The resulting annotations were used for downstream biological interpretation and T-cell-specific IRC analysis.

Annotation confidence was also recorded.

---

# 09 — IFN-I Response Score

**Script:** `scripts/09_irc_score.py`

A transcriptomic IFN-I response score was calculated using six genes associated with the experimental IFN-I response framework:

* **BST2**
* **EIF2AK2**
* **ISG15**
* **MX1**
* **IFIT3**
* **IRF7**

The score was calculated using Scanpy's `score_genes()` function.

Both continuous IRC scores and IRC High/Low classifications were generated.

---

# IRC Gene Set

The transcriptomic IRC gene set used in this project is:

```text
BST2
EIF2AK2
ISG15
MX1
IFIT3
IRF7
```

These six genes correspond to the IFN-stimulated proteins used in the experimental IRC framework of the primary publication.

---

# Experimental IRC vs Transcriptomic IRC

An important distinction must be made between the **experimental IRC** described in the primary publication and the **transcriptomic IRC** calculated in this project.

The original experimental IRC was based on the change between IFN-stimulated and unstimulated **protein measurements** for six IFN-stimulated proteins:

* BST2
* PKR/EIF2AK2
* MX1
* IFIT3
* IRF7
* ISG15

In contrast, this project calculates a score from **single-cell transcriptomic data** using the corresponding six genes.

Therefore:

> The IRC used in this project should be interpreted as a **transcriptional proxy for IFN-I responsiveness**, rather than a direct reproduction of the original experimental protein-based IRC.

---

# 10 — T-cell-specific IRC Validation

**Script:** `scripts/10_tcell_irc_validation.py`

IRC analysis was restricted to T cells to investigate IFN-I responsiveness within the T-cell population.

The analysis identified:

**20,315 T cells**

A T-cell-specific median split was used to classify cells into IRC-High and IRC-Low groups.

### T-cell IRC groups

| Group     |      Cells |
| --------- | ---------: |
| IRC-High  |     10,158 |
| IRC-Low   |     10,157 |
| **Total** | **20,315** |

The T-cell analysis included the following categories:

* Cytotoxic NK/T
* Cytotoxic T/NK
* Memory CD4/GZMK
* Naive/memory
* Naive/resting
* Treg-like/activated CD4

---

# 11 — IRC Differential Expression

**Script:** `scripts/11_irc_differential_expression.py`

Wilcoxon differential expression analysis was performed between IRC-High and IRC-Low T cells.

The analysis considered:

**31,120 genes**

### Differential expression results

At FDR < 0.05:

* **354 significant genes**
* **285 genes higher in IRC-High**
* **69 genes higher in IRC-Low**

Representative genes among the strongest differential-expression results included:

* EIF2AK2
* BST2
* MX1
* ISG15
* RNF213
* STAT1
* PARP14
* ACTB
* HLA-B
* B2M
* EPSTI1
* XAF1
* HLA-A
* IFI44
* IRF7

---

# 12 — Gene Set Enrichment Analysis

**Script:** `scripts/12_gsea_irc.py`

Gene set enrichment analysis was performed using GSEApy preranked analysis.

### GSEA settings

| Parameter           | Setting                 |
| ------------------- | ----------------------- |
| Ranking statistic   | Wilcoxon test statistic |
| Gene set collection | Hallmark 2020           |
| Permutations        | 1,000                   |

### Significant pathways

| Pathway                   |   NES |    FDR |
| ------------------------- | ----: | -----: |
| Interferon Alpha Response | 1.882 | <0.001 |
| Interferon Gamma Response | 1.834 | <0.001 |
| Allograft Rejection       | 1.614 |  0.007 |
| Oxidative Phosphorylation | 1.565 |  0.012 |
| MYC Targets V1            | 1.481 |  0.035 |

The strongest enrichment was observed for **Interferon Alpha Response**, followed by **Interferon Gamma Response**.

Overall, these results support a strong interferon-associated transcriptional program in IRC-High T cells.

### GSEA ranking limitation

Approximately **38.66% of genes had duplicated ranking statistics**.

Substantial ties in the ranking statistic can introduce arbitrary ordering among genes with identical values and should therefore be considered when interpreting the preranked GSEA results.

---

# 13 — T-cell Subtype IRC Validation

**Script:** `scripts/13_subtype_irc_validation.py`

IRC-High versus IRC-Low differential expression was evaluated separately within individual T-cell subtypes.

Subtypes with fewer than 10 cells in the relevant comparison groups were skipped.

### T-cell subtype results

| T-cell subtype          | IRC-High | IRC-Low | Significant genes |
| ----------------------- | -------: | ------: | ----------------: |
| Cytotoxic NK/T          |    1,435 |   1,256 |                 4 |
| Cytotoxic T/NK          |    1,755 |   1,446 |                16 |
| Memory CD4/GZMK         |      716 |     641 |                 4 |
| Naive/memory            |      968 |   1,167 |                 4 |
| Naive/resting           |    4,468 |   4,637 |               361 |
| Treg-like/activated CD4 |      816 |   1,010 |                14 |

In the analyzed subtypes, the six IRC genes were higher in IRC-High cells where they were reported as significant.

---

# Main Results

Following quality control and preprocessing:

* **94,513 cells** were retained.
* **31,120 genes** remained.
* **2,500 highly variable genes** were selected.
* **32 Leiden clusters** were identified.
* **20,315 T cells** were identified.

T-cell-specific IRC classification produced:

* **10,158 IRC-High T cells**
* **10,157 IRC-Low T cells**

Differential expression analysis identified:

* **354 significant genes**
* **285 genes higher in IRC-High**
* **69 genes higher in IRC-Low**

Hallmark GSEA identified significant enrichment of:

1. Interferon Alpha Response
2. Interferon Gamma Response
3. Allograft Rejection
4. Oxidative Phosphorylation
5. MYC Targets V1

These findings support the presence of a strong interferon-associated transcriptional program in the IRC-High T-cell population.

---

# Important Interpretation Notes

## IRC gene circularity

The six IRC genes are directly included in the score definition.

Therefore, differential expression of these same six genes between IRC-High and IRC-Low cells is expected and should **not** be considered independent validation of the IRC score.

Interpretation should instead emphasize:

* Independent IFN-associated genes
* Broader transcriptional programs
* Gene set enrichment results
* Consistency across T-cell populations and subtypes

---

## IRC cutoff

IRC-High and IRC-Low groups were defined using a **median-based cutoff**.

This is a relative classification within the analyzed population and should not be interpreted as an experimentally validated biological threshold.

---

## Cell-type annotation

Cell-type labels were assigned using transcriptomic marker expression.

Leiden cluster numbers do not inherently represent biological cell types.

Therefore, biological interpretation should be based on marker-gene evidence rather than cluster numbers alone.

---

## Clinical response

No patient-level clinical responder/non-responder analysis was performed.

Clinical responder/non-responder metadata were not available for this analysis.

Therefore, this project does **not** claim to predict individual patient response to PD-1 blockade therapy.

---

# Limitations

The major limitations of the current analysis are:

1. The transcriptomic IRC score is a proxy and does not directly reproduce the experimental protein-based IRC.
2. The six IRC genes are included in the score itself, creating circularity when those same genes are tested by differential expression.
3. The IRC cutoff was based on a median split rather than an experimentally validated biological threshold.
4. Cell-type annotation is based on transcriptomic marker expression and was not independently validated experimentally in this project.
5. The GSEA ranking contained substantial tied statistics.
6. Clinical responder/non-responder metadata were unavailable, preventing direct patient-level response prediction.
7. The analysis uses baseline PBMC samples and therefore does not directly measure treatment-induced transcriptional changes.
8. The observed associations do not establish causality between IFN-I responsiveness and immunotherapy outcome.

---

# Repository Structure

```text
PROJECT_3_IFN_I/
│
├── data/
│   └── 10x Genomics input data
│
├── docs/
│   ├── AI_USAGE_DISCLOSURE_PROJECT_3_IFN_I.md
│   ├── FIGURE_CAPTIONS.md
│   ├── FIGURE_MAPPING.md
│   ├── FIGURE_ORGANIZATION_README.md
│   ├── FINAL_ANALYSIS_VALIDATION.md
│   ├── GSEA_FIGURE_NOTES.md
│   ├── PIPELINE_DOCUMENTATION.md
│   ├── README_PROJECT.md
│   ├── RESULTS_SUMMARY.md
│   └── final report documents
│
├── figures/
│   └── final/
│       ├── Figure 1
│       ├── Figure 2
│       ├── Figure 3
│       ├── Figure 4
│       ├── Figure 5
│       ├── Figure 6
│       └── Supplementary Figures
│
├── results/
│   ├── differential-expression results
│   ├── marker-gene results
│   ├── IRC results
│   ├── GSEA results
│   └── AnnData objects
│
├── scripts/
│   ├── 01_validate_10x_data.py
│   ├── 02_load_combine.py
│   ├── 03_qc_filter.py
│   ├── 04_normalization_hvg.py
│   ├── 05_pca_umap_clustering.py
│   ├── 06_marker_genes.py
│   ├── 06b_full_gene_markers.py
│   ├── 07_marker_dotplot.py
│   ├── 08_annotate_cells.py
│   ├── 09_irc_score.py
│   ├── 10_tcell_irc_validation.py
│   ├── 11_irc_differential_expression.py
│   ├── 12_gsea_irc.py
│   └── 13_subtype_irc_validation.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Reproducibility

The analysis was implemented using the Python single-cell analysis ecosystem.

Major software packages include:

* Python
* Scanpy
* AnnData
* NumPy
* pandas
* SciPy
* matplotlib
* seaborn
* GSEApy

Package requirements are documented in:

`requirements.txt`

The numbered scripts are designed to be executed sequentially.

The general workflow is:

```text
01_validate_10x_data.py
        ↓
02_load_combine.py
        ↓
03_qc_filter.py
        ↓
04_normalization_hvg.py
        ↓
05_pca_umap_clustering.py
        ↓
06_marker_genes.py
        ↓
06b_full_gene_markers.py
        ↓
07_marker_dotplot.py
        ↓
08_annotate_cells.py
        ↓
09_irc_score.py
        ↓
10_tcell_irc_validation.py
        ↓
11_irc_differential_expression.py
        ↓
12_gsea_irc.py
        ↓
13_subtype_irc_validation.py
```

Large intermediate AnnData files are excluded from Git version control using `.gitignore` to keep the public repository lightweight.

---

# Results and Data Organization

The `results/` directory contains analysis outputs including:

* Processed AnnData objects
* Cluster marker-gene tables
* Full-gene marker tables
* IRC scores
* IRC differential-expression results
* T-cell subtype results
* GSEA results
* Supporting CSV files

Large `.h5ad` files are intentionally excluded from GitHub through `.gitignore`.

---

# Figures

Final figures are organized under:

```text
figures/final/
```

The project includes final main figures and supplementary figures.

Figure descriptions and organization are documented in:

* `docs/FIGURE_CAPTIONS.md`
* `docs/FIGURE_MAPPING.md`
* `docs/FIGURE_ORGANIZATION_README.md`
* `docs/GSEA_FIGURE_NOTES.md`

---

# Documentation

Additional documentation is available in the `docs/` directory.

Important documents include:

### Pipeline Documentation

`docs/PIPELINE_DOCUMENTATION.md`

Provides detailed information about the computational workflow, parameters, and analysis decisions.

### Results Summary

`docs/RESULTS_SUMMARY.md`

Provides a concise summary of the major quantitative findings.

### Final Analysis Validation

`docs/FINAL_ANALYSIS_VALIDATION.md`

Documents validation and interpretation checks performed during the final analysis.

### Figure Documentation

Figure captions, figure mapping, and figure organization are documented separately in the `docs/` directory.

### AI Usage Disclosure

`docs/AI_USAGE_DISCLOSURE_PROJECT_3_IFN_I.md`

Documents the use of AI-assisted tools during project development and analysis.

---

# Final Report

The project includes a final report documenting:

* Scientific background
* Dataset
* Methods
* Quality control
* Clustering
* Cell-type annotation
* IRC analysis
* Differential expression
* GSEA
* Subtype validation
* Interpretation
* Limitations
* Conclusions

The final report is maintained separately from the computational scripts and GitHub README.

---

# Version Control

This project is maintained using Git and GitHub.

The repository uses the `main` branch.

Large data and intermediate analysis files are excluded from version control using `.gitignore`.

The repository is intended to provide a transparent record of the computational workflow while avoiding unnecessary storage of large intermediate files.

---

# Primary Reference

**Pre-encoded responsiveness to type I interferon in the peripheral immune system defines outcome of PD1 blockade therapy.**

*Nature Immunology*, 2022.

**Public dataset:** GSE199994

The publication provides the biological motivation for investigating pre-existing IFN-I responsiveness in peripheral immune cells in relation to PD-1 blockade therapy.

---

# Project Status

**Status: Analysis completed**

The project includes:

* 10x Genomics data validation
* Sample loading and combination
* Quality control
* Normalization
* Highly variable gene selection
* PCA
* Neighborhood graph construction
* UMAP
* Leiden clustering
* Marker-gene analysis
* Full-gene marker analysis
* Cell-type annotation
* Transcriptomic IFN-I response scoring
* T-cell-specific IRC analysis
* Differential expression
* Hallmark GSEA
* T-cell subtype validation
* Final figures
* Final report
* Project documentation
* Git version control
* GitHub repository

---

# AI Usage

AI-assisted tools were used during aspects of project development, including:

* Code drafting
* Code debugging
* Error interpretation
* Workflow organization
* Documentation assistance
* Interpretation support

AI assistance was used as a technical and documentation aid. Analysis execution, result verification, scientific decisions, and final interpretation remained the responsibility of the project author.

Detailed disclosure is provided in:

`docs/AI_USAGE_DISCLOSURE_PROJECT_3_IFN_I.md`

---

# Author

**Md Osman Gani Bhuiyan**

**Project 3 — Type I Interferon Immunotherapy Response**

---

# License

No open-source license is currently specified for this repository.

