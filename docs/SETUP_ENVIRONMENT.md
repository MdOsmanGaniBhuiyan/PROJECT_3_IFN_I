# PROJECT_3_IFN_I — Environment Setup

This document records the computational environment used for the
`PROJECT_3_IFN_I` single-cell RNA-seq analysis.

## 1. System

- Host OS: Windows
- Linux environment: WSL2
- Distribution: Ubuntu
- Project path: `/mnt/c/bio/PROJECT_3_IFN_I`

Check WSL:

```powershell
wsl --status
wsl --list --verbose
```

Check Ubuntu:

```bash
lsb_release -a
uname -a
```

## 2. Ubuntu System Packages

Update Ubuntu and install the required system tools:

```bash
sudo apt update
sudo apt upgrade -y

sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    unzip \
    zip \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv
```

## 3. Git

Check Git:

```bash
git --version
```

Configure Git identity:

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
```

Check:

```bash
git config --global --list
```

## 4. Python

Check Python and pip:

```bash
python3 --version
python3 -m pip --version
```

## 5. Project Environment

Go to the project:

```bash
cd /mnt/c/bio/PROJECT_3_IFN_I
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

## 6. Python Packages

Install the packages required for the scRNA-seq workflow:

```bash
pip install \
    scanpy \
    anndata \
    numpy \
    pandas \
    scipy \
    matplotlib \
    seaborn \
    scikit-learn \
    umap-learn \
    igraph \
    leidenalg
```

## 7. Verify the Environment

With the virtual environment activated:

```bash
python -c "
import scanpy as sc
import anndata
import numpy
import pandas
import scipy
import matplotlib
import seaborn
import sklearn
import umap
import igraph
import leidenalg

print('Environment OK')
print('Scanpy:', sc.__version__)
print('AnnData:', anndata.__version__)
print('Python:', __import__('sys').version.split()[0])
"
```

## 8. Save Exact Package Versions

After the environment is finalized:

```bash
pip freeze > requirements.txt
```

`requirements.txt` records the exact Python package versions used by the
project.

## 9. Reproduce the Python Environment

On another computer, after installing WSL2, Ubuntu, Python and the required
system tools:

```bash
cd /mnt/c/bio/PROJECT_3_IFN_I
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 10. Project Structure

```text
PROJECT_3_IFN_I/
├── data/
├── scripts/
├── results/
├── figures/
├── docs/
│   └── SETUP_ENVIRONMENT.md
├── requirements.txt
└── README.md
```

## 11. Environment Activation

Before running the analysis:

```bash
cd /mnt/c/bio/PROJECT_3_IFN_I
source .venv/bin/activate
```

Verify:

```bash
which python
```

The Python executable should be inside the project's `.venv` directory.


