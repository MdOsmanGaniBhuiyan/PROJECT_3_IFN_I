# Reproducing the Environment on Another Computer

The general procedure for reproducing this project is:

### Step 1 — Install WSL2

From Windows PowerShell:

```powershell
wsl --install
```

Restart if required.

### Step 2 — Install/launch Ubuntu

Check:

```powershell
wsl --list --verbose
```

Confirm Ubuntu is using WSL2.

### Step 3 — Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 4 — Install system dependencies

```bash
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

### Step 5 — Obtain the project

Clone the GitHub repository:

```bash
git clone MY_REPOSITORY_URL
```

Then enter the project:

```bash
cd PROJECT_3_IFN_I
```

### Step 6 — Create the Python environment

```bash
python3 -m venv .venv
```

### Step 7 — Activate it

```bash
source .venv/bin/activate
```

### Step 8 — Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 9 — Install project dependencies

```bash
pip install -r requirements.txt
```

### Step 10 — Verify

```bash
python -c "import scanpy as sc; print(sc.__version__)"
```

Then run the environment verification command described above.