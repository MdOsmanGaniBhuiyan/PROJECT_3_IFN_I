# PROJECT 3 --- Git/GitHub Workflow Record

## Type I Interferon Immunotherapy Response --- Single-Cell RNA-seq Analysis

**Repository:** `PROJECT_3_IFN_I`\
**Local project path:** `/mnt/c/bio/PROJECT_3_IFN_I`\
**GitHub repository:** `MdOsmanGaniBhuiyan/PROJECT_3_IFN_I`\
**Default branch:** `main`

------------------------------------------------------------------------

## 1. Purpose of This Document

This document is a detailed record of the Git/GitHub workflow used for
PROJECT_3_IFN_I.

The goal is not only to record the final commands, but also to preserve:

-   what we did,
-   why we did it,
-   what problems occurred,
-   how those problems were fixed,
-   what files were intentionally included or excluded,
-   how authentication was handled,
-   how the README was created,
-   what was verified,
-   where the workflow stopped, and
-   what the final repository state was.

This is intended as a reproducibility and learning record for future
Git/GitHub work.

> **Important:** The record below is based on the PROJECT_3_IFN_I
> conversation history and the final terminal audit. Where an exact
> historical command was not preserved in the available conversation
> record, the step is described rather than presented as a verbatim
> command.

------------------------------------------------------------------------

# Part I --- Project Preparation Before Git

## 2. Project Context Before GitHub

Before GitHub setup, PROJECT_3_IFN_I had already undergone substantial
single-cell RNA-seq analysis.

The project contained:

``` text
PROJECT_3_IFN_I/
├── data/
├── docs/
├── figures/
├── results/
├── scripts/
└── requirements.txt
```

The project included:

-   10x Genomics single-cell input data
-   QC and preprocessing scripts
-   PCA/UMAP/Leiden clustering
-   marker-gene analysis
-   cell-type annotation
-   IFN-I IRC scoring
-   T-cell IRC analysis
-   differential expression
-   GSEA
-   subtype validation
-   final figures
-   final report
-   documentation

Large intermediate AnnData files were present locally, including files
on the order of hundreds of MB to several GB.

This became an important consideration when designing the Git workflow.

------------------------------------------------------------------------

## 3. Analysis Fixes and Patches That Happened Before/Alongside Git Documentation

The project was not simply uploaded unchanged. During development,
scripts were debugged and compatibility issues were corrected.

One documented example was a correction in the GSEA script:

``` bash
sed -i 's/de\[\["gene", "scores", "logfoldchange"\]\]/de[["gene", "score", "logfoldchange"]]/g' scripts/12_gsea_irc.py
```

This corrected the expected column name from `scores` to `score`.

The project history also included debugging around:

-   GSEApy compatibility,
-   ranking columns,
-   Scanpy analysis,
-   shell commands,
-   QC execution,
-   intermediate result generation.

These fixes mattered because the repository was intended to contain the
working analysis scripts rather than abandoned or broken versions.

------------------------------------------------------------------------

# Part II --- Initialize Git

## 4. Enter the Project Directory

The Git work was performed from WSL.

The working directory was:

``` bash
cd /mnt/c/bio/PROJECT_3_IFN_I
```

The project prompt was:

``` text
(PROJECT_3_IFN_I) (base) osman@BlueSky:/mnt/c/bio/PROJECT_3_IFN_I$
```

------------------------------------------------------------------------

## 5. Check Git Version

Git was available in the WSL environment.

The Git version observed was:

``` text
git version 2.53.0
```

------------------------------------------------------------------------

## 6. Initialize the Repository

Command:

``` bash
git init
```

### Why?

This converted the local project directory into a Git repository.

It created the `.git/` directory that stores Git's version-control
information.

------------------------------------------------------------------------

## 7. Rename the Branch to `main`

Command:

``` bash
git branch -M main
```

### Why?

The project was standardized on the `main` branch.

This also made the local branch name match the intended GitHub default
branch.

------------------------------------------------------------------------

# Part III --- Protect Large and Sensitive Files

## 8. Create `.gitignore`

Before staging the project, a `.gitignore` file was created.

This was one of the most important parts of the workflow because the
project contained very large single-cell data files.

The final `.gitignore` includes protections for:

### Python environments

``` text
.venv/
venv/
env/
.env
```

### Python cache

``` text
__pycache__/
*.py[cod]
*.pyo
```

### Jupyter

``` text
.ipynb_checkpoints/
```

### OS/editor files

``` text
.DS_Store
Thumbs.db
.vscode/
.idea/
```

### Logs

``` text
logs/
*.log
```

### Raw single-cell data

``` text
data/
```

### Large AnnData objects

``` text
results/*.h5ad
results/**/*.h5ad
```

### Large/intermediate bioinformatics files

``` text
*.mtx
*.mtx.gz
*.h5
*.hdf5
*.loom
```

### Sequencing files

``` text
*.fastq
*.fastq.gz
*.fq
*.fq.gz
```

### Temporary files

``` text
*.tmp
*.temp
*.swp
*.bak
```

### Lightweight results retained

``` text
!results/*.csv
!results/gsea/*.csv
!results/gsea/*.rnk
```

### Final figures retained

``` text
!figures/
!figures/final/
!figures/final/**/*.png
!figures/final/**/*.pdf
```

### Working figures excluded

The generated/working figures in the root `figures/` directory were
excluded individually.

### Old report versions excluded

Only the official final report was retained.

### Generated GSEA reports excluded

Generated duplicate GSEA report directories/files were excluded.

------------------------------------------------------------------------

## 9. Why `.gitignore` Was Necessary

The project had very large `.h5ad` files.

Examples from the local project included approximately:

``` text
adata_annotated_full.h5ad       ~904 MB
adata_full_gene_markers.h5ad    ~2.0 GB
adata_irc_scored.h5ad           ~905 MB
adata_markers.h5ad              ~2.0 GB
adata_normalized_hvg.h5ad       ~3.0 GB
adata_pca_umap_leiden.h5ad      ~2.0 GB
adata_qc_filtered.h5ad          ~1.5 GB
adata_tcell_irc.h5ad            ~192 MB
```

The complete local results directory was roughly 13 GB.

Uploading these files to a normal GitHub repository would be
inappropriate for this project.

Therefore the strategy was:

**Keep locally:**

-   raw data,
-   large AnnData objects,
-   large intermediate files.

**Track in Git/GitHub:**

-   Python scripts,
-   documentation,
-   final figures,
-   lightweight CSV results,
-   selected GSEA ranking/result files,
-   README,
-   requirements.

------------------------------------------------------------------------

# Part IV --- Verify Before Staging

## 10. Dry-run `git add`

Command:

``` bash
git add -n .
```

### Why?

This was deliberately done before the real `git add`.

The dry run allowed us to inspect what Git intended to stage.

This was especially important because the project contained
multi-gigabyte files.

The goal was to verify that:

-   scripts were included,
-   documentation was included,
-   figures were included,
-   lightweight results were included,
-   raw data were excluded,
-   `.h5ad` files were excluded.

------------------------------------------------------------------------

## 11. Stage the Project

Command:

``` bash
git add .
```

### Why?

This staged the project files that were allowed by `.gitignore`.

------------------------------------------------------------------------

# Part V --- Configure Git Identity

## 12. Configure Git Author Name

Command:

``` bash
git config --global user.name "Md Osman Gani Bhuiyan"
```

------------------------------------------------------------------------

## 13. Configure Git Author Email

Command:

``` bash
git config --global user.email "mdosmanganibhuiyan@gmail.com"
```

### Why?

Git stores author information inside commits.

These settings identify the author of the project commits.

------------------------------------------------------------------------

# Part VI --- First Commit

## 14. Create the Initial Commit

Command:

``` bash
git commit -m "Initial Project 3 IFN-I single-cell analysis"
```

Result:

``` text
235ccfd Initial Project 3 IFN-I single-cell analysis
```

The initial commit contained:

-   **77 files**
-   approximately **539,905 insertions**

### Why?

This created the first versioned snapshot of the project.

------------------------------------------------------------------------

## 15. Verify the Initial Working Tree

Command:

``` bash
git status
```

The working tree was clean after the initial commit.

This confirmed that the staged changes had been committed.

------------------------------------------------------------------------

# Part VII --- Create the GitHub Repository

## 16. Create the Remote GitHub Repository

GitHub repository:

``` text
PROJECT_3_IFN_I
```

Owner:

``` text
MdOsmanGaniBhuiyan
```

Repository:

``` text
https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I
```

### Repository choices

The repository was created as:

-   **Public**
-   README initialization: **Off**
-   GitHub-generated `.gitignore`: **Off**
-   License: **No License**

### Why?

The local project already contained its own README and `.gitignore`.

The local repository was therefore treated as the source of truth.

------------------------------------------------------------------------

# Part VIII --- Connect Local Git to GitHub

## 17. Add the GitHub Remote

Command:

``` bash
git remote add origin https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I.git
```

### Why?

This connected the local Git repository to the GitHub repository.

The remote was named:

``` text
origin
```

------------------------------------------------------------------------

## 18. Verify the Remote

Command:

``` bash
git remote -v
```

Final remote:

``` text
origin  https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I.git (fetch)
origin  https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I.git (push)
```

------------------------------------------------------------------------

# Part IX --- First GitHub Push and Authentication Problem

## 19. Attempt the Initial Push

Command:

``` bash
git push -u origin main
```

The first push failed because GitHub password authentication was
attempted.

The error was:

``` text
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed
```

### Why did this happen?

GitHub no longer accepts the normal account password for Git operations
over HTTPS.

A supported authentication method was required.

------------------------------------------------------------------------

# Part X --- Fine-grained Personal Access Token

## 20. Create a Fine-grained PAT

A GitHub fine-grained Personal Access Token was created.

Configuration:

  Setting             Value
  ------------------- ------------------------
  Token name          `PROJECT_3_IFN_I_WSL`
  Owner               `MdOsmanGaniBhuiyan`
  Repository access   Only `PROJECT_3_IFN_I`
  Contents            Read and write
  Metadata            Read-only
  Expiration          30 days

### Why this configuration?

The token was intentionally restricted to the project repository rather
than granting broad repository access.

The token itself was **not shared** in the conversation and should never
be committed to the repository.

------------------------------------------------------------------------

# Part XI --- Successful Initial Push

## 21. Push Again

Command:

``` bash
git push -u origin main
```

The push succeeded.

The remote reported:

``` text
To https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I.git
 * [new branch] main -> main
branch 'main' set up to track 'origin/main'.
```

Approximately 20.27 MiB was transferred.

### Why is this important?

The local project contained approximately 13 GB of results/intermediate
data, but only about 20 MB was transferred.

This strongly supported that the `.gitignore` strategy was working.

------------------------------------------------------------------------

# Part XII --- Verify the First GitHub State

## 22. Check Git Status

Command:

``` bash
git status
```

The local branch was synchronized with the remote.

------------------------------------------------------------------------

## 23. Check Git History

Command:

``` bash
git log --oneline --max-count=3
```

The important initial state was:

``` text
235ccfd (HEAD -> main, origin/main) Initial Project 3 IFN-I single-cell analysis
```

This showed that:

``` text
local main == origin/main
```

------------------------------------------------------------------------

# Part XIII --- Build the Professional README

## 24. Why We Added a README

After the initial GitHub upload, the repository needed a professional
entry point.

The README was designed to explain:

-   the biological question,
-   dataset,
-   analysis workflow,
-   scripts,
-   IRC gene set,
-   main results,
-   GSEA,
-   interpretation caveats,
-   repository structure,
-   reproducibility,
-   figures,
-   documentation,
-   limitations,
-   reference,
-   AI usage,
-   project status.

------------------------------------------------------------------------

## 25. README Development Issue

The first attempt to write the very long README using a large shell
heredoc was inconvenient because the terminal showed the continuation
prompt:

``` text
>
```

The command was therefore stopped/adjusted rather than continuing with
an unreliable long paste.

A smaller/safer editing approach was then used.

This was one reason the README work took additional time.

------------------------------------------------------------------------

## 26. README Content

The final README became a comprehensive project document.

It includes:

-   Project title
-   Single-cell RNA-seq description
-   Dataset
-   Analysis workflow
-   All numbered analysis scripts
-   QC parameters
-   PCA/UMAP/Leiden parameters
-   IRC gene set
-   Experimental IRC vs transcriptomic IRC distinction
-   T-cell IRC analysis
-   DE results
-   GSEA results
-   subtype analysis
-   interpretation notes
-   limitations
-   repository structure
-   reproducibility
-   results organization
-   figures
-   documentation
-   final report
-   version control
-   primary reference
-   project status
-   AI usage
-   author
-   license status

------------------------------------------------------------------------

# Part XIV --- README Commit

## 27. Stage the README

Command:

``` bash
git add README.md
```

------------------------------------------------------------------------

## 28. Commit the README

Command:

``` bash
git commit -m "Add comprehensive project README"
```

Result:

``` text
37ad22e Add comprehensive project README
```

The commit added:

``` text
838 insertions(+)
```

------------------------------------------------------------------------

# Part XV --- README Push Authentication Problem

## 29. First README Push Attempt

Command:

``` bash
git push
```

The first attempt again failed because an invalid password was entered.

The error was:

``` text
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed
```

### Important

This did **not** damage the README commit.

The commit already existed locally.

The only problem was authentication during the push.

------------------------------------------------------------------------

# Part XVI --- Successful README Push

## 30. Retry the Push

Command:

``` bash
git push
```

The second attempt succeeded.

Result:

``` text
To https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I.git
   235ccfd..37ad22e  main -> main
```

Therefore the README was successfully published to GitHub.

------------------------------------------------------------------------

# Part XVII --- Verify the README

## 31. Check the README Beginning

Command:

``` bash
head -10 README.md
```

The README begins with:

``` text
# PROJECT 3 — Type I Interferon Immunotherapy Response

## Single-Cell RNA-seq Analysis
```

------------------------------------------------------------------------

## 32. Check README Length

Command:

``` bash
wc -l README.md
```

Result:

``` text
838 README.md
```

------------------------------------------------------------------------

## 33. Check README Git History

Command:

``` bash
git log --oneline -- README.md
```

Result:

``` text
37ad22e (HEAD -> main, origin/main) Add comprehensive project README
```

This confirmed that the README was committed and that the commit was
present locally and remotely.

------------------------------------------------------------------------

# Part XVIII --- Final Repository Audit

## 34. Final `git status`

Command:

``` bash
git status
```

Final result:

``` text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

This is the desired final state.

------------------------------------------------------------------------

# 35. Inspect All Tracked Files

Command:

``` bash
git ls-files
```

The final tracked repository included:

### Root files

``` text
.gitignore
README.md
requirements.txt
```

### Documentation

``` text
docs/AI_USAGE_DISCLOSURE_PROJECT_3_IFN_I.md
docs/FIGURE_CAPTIONS.md
docs/FIGURE_MAPPING.md
docs/FIGURE_ORGANIZATION_README.md
docs/FINAL_ANALYSIS_VALIDATION.md
docs/GSEA_FIGURE_NOTES.md
docs/PIPELINE_DOCUMENTATION.md
docs/PROJECT_3_IFN_I_FINAL.docx
docs/README_PROJECT.md
docs/RESULTS_SUMMARY.md
```

### Analysis scripts

All 14 project scripts were tracked:

``` text
scripts/01_validate_10x_data.py
scripts/02_load_combine.py
scripts/03_qc_filter.py
scripts/04_normalization_hvg.py
scripts/05_pca_umap_clustering.py
scripts/06_marker_genes.py
scripts/06b_full_gene_markers.py
scripts/07_marker_dotplot.py
scripts/08_annotate_cells.py
scripts/09_irc_score.py
scripts/10_tcell_irc_validation.py
scripts/11_irc_differential_expression.py
scripts/12_gsea_irc.py
scripts/13_subtype_irc_validation.py
```

### Final figures

Main and supplementary final figures were tracked, including:

``` text
Figure_1_QC.png
Figure_2A_UMAP_Leiden_clusters.png
Figure_2B_UMAP_annotated_cell_types.png
Figure_3_marker_dotplot.png
Figure_4A_IRC_score_UMAP.png
Figure_4B_IRC_status_UMAP.png
Figure_4C_IRC_score_by_cell_type.png
Figure_5A_Tcell_IRC_status_UMAP.png
Figure_5B_Tcell_IRC_score_by_subtype.png
Figure_6_GSEA.png
```

along with supplementary figures and individual GSEA PDFs.

### Lightweight results

Tracked results included CSV and RNK files such as:

``` text
results/cluster_annotations.csv
results/cluster_marker_genes.csv
results/cluster_top20_markers.csv
results/full_gene_marker_genes.csv
results/full_gene_top20_markers.csv
results/irc_high_vs_low_de.csv
results/irc_scores_per_cell.csv
results/irc_summary_by_cell_type.csv
results/subtype_irc_de_all_genes.csv
results/subtype_irc_de_summary.csv
results/tcell_irc_summary.csv
results/gsea/hallmark_gsea_results.csv
results/gsea/irc_high_enriched_hallmark.csv
results/gsea/irc_low_enriched_hallmark.csv
```

------------------------------------------------------------------------

# 36. Verify Large Files Were NOT Tracked

Command:

``` bash
git ls-files | grep -E '\.(h5ad|h5|loom|mtx|fastq|fastq\.gz)$'
```

Result:

``` text
```

There was no output.

### Interpretation

No files with these large/raw-data extensions were tracked by Git.

This confirmed that the `.gitignore` protection was working.

------------------------------------------------------------------------

# 37. Verify `.gitignore`

Command:

``` bash
cat .gitignore
```

The final `.gitignore` was inspected and confirmed to contain the
intended protections for:

-   raw data,
-   large AnnData objects,
-   sequencing files,
-   intermediate formats,
-   working figures,
-   old reports,
-   generated GSEA files,
-   temporary files.

------------------------------------------------------------------------

# 38. Verify Commit History

Command:

``` bash
git log --oneline --decorate --graph --all
```

Final history:

``` text
* 37ad22e (HEAD -> main, origin/main) Add comprehensive project README
* 235ccfd Initial Project 3 IFN-I single-cell analysis
```

This is a clean and simple two-commit history.

------------------------------------------------------------------------

# 39. Verify GitHub Remote

Command:

``` bash
git remote -v
```

Final result:

``` text
origin  https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I.git (fetch)
origin  https://github.com/MdOsmanGaniBhuiyan/PROJECT_3_IFN_I.git (push)
```

------------------------------------------------------------------------

# Part XIX --- Final State

## 40. Final Git State

At the end of the workflow:

``` text
Branch:
main

Remote:
origin

Tracking:
main -> origin/main

Working tree:
clean

README:
committed and pushed

Scripts:
tracked

Documentation:
tracked

Final figures:
tracked

Lightweight results:
tracked

Raw data:
ignored

Large AnnData files:
ignored

GitHub:
synchronized
```

------------------------------------------------------------------------

# 41. Final Git History

``` text
37ad22e  Add comprehensive project README
235ccfd  Initial Project 3 IFN-I single-cell analysis
```

------------------------------------------------------------------------

# 42. Where We Stopped

We stopped the Git/GitHub workflow here.

The repository was considered **GitHub-ready**.

No additional Git commit or push was required at this point.

The final state was:

``` text
HEAD -> main
origin/main
```

both pointing to:

``` text
37ad22e
```

and:

``` text
working tree clean
```

------------------------------------------------------------------------

# 43. Why We Stopped

We stopped because the original Git objective had been achieved.

The project now had:

1.  A local Git repository.
2.  A `main` branch.
3.  A carefully designed `.gitignore`.
4.  A complete initial commit.
5.  A public GitHub repository.
6.  A configured `origin` remote.
7.  Working GitHub authentication using a fine-grained PAT.
8.  A comprehensive README.
9.  Version-controlled analysis scripts.
10. Version-controlled documentation.
11. Version-controlled final figures.
12. Version-controlled lightweight result tables.
13. Protection against uploading the large raw/intermediate data.
14. A clean Git history.
15. A synchronized local and remote branch.

Continuing to modify Git configuration without a new requirement would
not provide additional value.

The next stage therefore moves back to **scientific final validation of
the single-cell analysis**, rather than further Git setup.

------------------------------------------------------------------------

# Part XX --- Security Notes

## 44. Personal Access Token

The fine-grained PAT was used only for authentication.

The token itself should never be:

-   committed,
-   placed in README,
-   placed in scripts,
-   placed in `.gitignore`,
-   shared publicly,
-   pasted into GitHub issues,
-   stored in project documentation.

The PAT created during this workflow had a **30-day expiration**.

If GitHub authentication stops working after expiration, a new supported
authentication method/token may be needed.

------------------------------------------------------------------------

# Part XXI --- Useful Commands for Future Changes

## 45. Check Status

``` bash
git status
```

Use this before and after making changes.

------------------------------------------------------------------------

## 46. Inspect Changes

``` bash
git diff
```

Use this to inspect modifications before committing.

------------------------------------------------------------------------

## 47. Stage a Specific File

``` bash
git add <filename>
```

Example:

``` bash
git add scripts/12_gsea_irc.py
```

------------------------------------------------------------------------

## 48. Commit a Change

``` bash
git commit -m "Describe the change"
```

Good commit messages should describe what changed.

Examples:

``` text
Fix GSEA ranking column
Update IRC analysis documentation
Add supplementary figure
```

------------------------------------------------------------------------

## 49. Push Changes

``` bash
git push
```

Because `main` already tracks `origin/main`, the simple command is
sufficient.

------------------------------------------------------------------------

## 50. View History

``` bash
git log --oneline --decorate --graph --all
```

------------------------------------------------------------------------

## 51. Check Remote

``` bash
git remote -v
```

------------------------------------------------------------------------

## 52. Check Whether Large Files Are Tracked

``` bash
git ls-files | grep -E '\.(h5ad|h5|loom|mtx|fastq|fastq\.gz)$'
```

If there is no output, none of those file types are currently tracked.

------------------------------------------------------------------------

# Part XXII --- Final Checklist

The Git/GitHub workflow completed the following:

-   [x] Git initialized
-   [x] `main` branch configured
-   [x] `.gitignore` created
-   [x] `.gitignore` tested with dry-run staging
-   [x] Raw data protected
-   [x] Large `.h5ad` files protected
-   [x] Sequencing files protected
-   [x] Working/generated files protected
-   [x] Git identity configured
-   [x] Initial project staged
-   [x] Initial commit created
-   [x] GitHub repository created
-   [x] Repository made public
-   [x] GitHub README initialization disabled
-   [x] GitHub-generated `.gitignore` disabled
-   [x] No license selected
-   [x] `origin` remote configured
-   [x] First authentication problem identified
-   [x] Fine-grained PAT created
-   [x] PAT restricted to PROJECT_3_IFN_I
-   [x] Initial push completed
-   [x] Comprehensive README created
-   [x] README committed
-   [x] README pushed
-   [x] README verified at 838 lines
-   [x] All 14 analysis scripts tracked
-   [x] Documentation tracked
-   [x] Final figures tracked
-   [x] Lightweight results tracked
-   [x] Large/raw data confirmed untracked
-   [x] Final Git history verified
-   [x] Remote verified
-   [x] Working tree confirmed clean
-   [x] `main` confirmed synchronized with `origin/main`

------------------------------------------------------------------------

# Final Conclusion

## PROJECT_3_IFN_I Git/GitHub Workflow: COMPLETE

The project now has a clean Git/GitHub structure suitable for
documenting and sharing the computational analysis.

The repository preserves the important reproducible components while
deliberately excluding the large raw and intermediate single-cell data
files.

The final known state is:

``` text
37ad22e (HEAD -> main, origin/main) Add comprehensive project README
235ccfd Initial Project 3 IFN-I single-cell analysis
```

``` text
main == origin/main
working tree clean
```

**Git/GitHub setup is complete.**

The next project stage is scientific final validation of the single-cell
analysis.
