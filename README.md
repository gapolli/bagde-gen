# 🛡️ Badge Gen

<!-- BADGES_START -->
<p align="center">
  <img src="https://shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Badge" />
  <img src="https://shields.io/badge/Bash-5.2-4EAA25?style=flat-square&logo=bash&logoColor=white" alt="Badge" />
  <img src="https://shields.io/badge/Open--Source-Community-success?style=flat-square&logo=open-source&logoColor=white" alt="Badge" />
  <img src="https://shields.io/badge/Maintained-Yes-blue?style=flat-square&logo=maintained&logoColor=white" alt="Badge" />
  <img src="https://shields.io/badge/Contributions-welcome-green?style=flat-square&logo=contributions&logoColor=white" alt="Badge" />
</p>
<!-- BADGES_END -->




A Command Line Interface (CLI) and Bash orchestration framework designed to automate the generation of dynamic and static badges for GitHub documentation. This toolkit bridges the gap between daily developer usage and hands-off CI/CD pipeline automation.

## 📁 Project Structure
```text
.
├── .env                         # Local private environment runtime configurations
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md        # Standardized tracking sheet for runtime anomalies
│   │   └── feature_request.md   # Architectural scope layout for modular additions
│   ├── pull_request_template.md # Contribution validation safety checklist
│   └── workflows/
│       └── ci.yml               # Automated pipeline suite (Lint, Test, Tag, Sync)
├── .gitignore                   # Isolation rule sheet preventing testing artifacts tracking
├── CONTRIBUTING.md              # Quality standards guidelines for external developers
├── Makefile                     # Compiler mapping shorthand terminal shortcuts
├── README.md                    # Primary system documentation entry point
├── badge_gen.py                 # Core Python rendering module and utility engine
├── badge_gen.sh                 # Adaptive Bash interface wrapper and automation driver
├── run_local_test.sh            # Manual multi-layered test pipeline emulator script
└── tests/
    ├── test_badge.py            # Unit validation suites covering edge boundaries
    └── test_integration.py      # End-to-end file persistence and shell simulation flows
```

## 📋 Table of Contents
- [📌 Quick Start](#-quick-start)
- [📋 Prerequisites](#-prerequisites)
- [🚀 Installation](#-installation)
- [⚙️ Environment Configuration](#-environment-configuration)
- [💡 Detailed Usage Guide](#-detailed-usage-guide)
  - [1. Static Technology Stack](#1-static-technology-stack)
  - [2. Dynamic Metrics](#2-dynamic-metrics)
  - [3. Batch Processing (Sections)](#3-batch-processing-sections)
- [🤖 CI/CD Automation](#-cicd-automation)
- [🔒 Security & Environment Auditing](#-security--environment-auditing)
- [🧹 Workspace Purging](#-workspace-purging)
- [🧪 Testing Suite](#-testing-suite)
- [📜 License](#-license)

---

## 📌 Quick Start
If you do not want to manage long Python commands or complex terminal flags, use our unified `Makefile` shorthand wrappers:

```bash
# 1. Install all system dependencies and verify environments
make install

# 2. Automatically check formatting rules and unit health profiles
make lint
make test

# 3. Inject, center, and align the default stable badges into this README header instantly
make top
```

---

## 📋 Prerequisites
- **Python 3.8** or higher.
- A **GitHub Personal Access Token** (required for repository footprints and traffic metrics).
- *(Optional)* **Snyk API Token** for vulnerability tracking metrics.
- *(Optional)* **UptimeRobot API Key** for live system latency mapping.

---

## 🚀 Installation
Initialize the ecosystem requirements using either our compiled shortcuts manager or traditional manual procedures:

### Automated Method (Recommended)
```bash
make install
```

### Manual Method
```bash
pip install requests python-dotenv requests-mock pytest pytest-cov black flake8
# Optional Windows OS native alerts engine support
pip install win10toast
```

---

## ⚙️ Environment Configuration
Initialize your API tokens and Webhook URLs securely before attempting to pull dynamic cloud queries:
```bash
make config
# Or manually via: python badge_gen.py setup
```
This routine safely compiles parameters inside an isolated `.env` configuration template.

---

## 💡 Detailed Usage Guide

The orchestration layer supports inline visual design overrides (`for-the-badge`, `flat`, `flat-square`, `plastic`, `social`) passed seamlessly before standard operation invocations.

### 1. Static Technology Stack
Static badges implement standard pre-defined hex boundaries for brand compliance.
```bash
# Shorthand Orchestrator Syntax (Auto logo calculation)
./badge_gen.sh flat-square tech Python "3.12"
./badge_gen.sh for-the-badge tech Docker "v24" "success"

# Advanced Core Engine Syntax
python badge_gen.py static --label "Python" --message "3.12" --logo "python" --style "flat" --color "3776AB"
```

### 2. Dynamic Metrics
Live data collection tracking build stability parameters and storage space properties.
```bash
# Shorthand Orchestrator Syntax
./badge_gen.sh metric repo-size [user] [repo]
./badge_gen.sh build [user] [repo]

# Advanced Core Engine Syntax
python badge_gen.py --hide-broken dynamic --type actions --user "user" --repo "repo" --workflow "ci.yml"
```

### 3. Batch Processing (Sections)
Map and construct an entirely localized group of multi-tier badges reading from a structured JSON blueprint:
```bash
./badge_gen.sh sync "Production Status" pipeline.json
```

---

## 🤖 CI/CD Automation
The engine auto-intercepts active CI virtualization boundaries (detecting parameters like `$CI` or `$GITHUB_ACTIONS`), suppressing local machine alerts to keep automation clean. It utilizes hidden comment tokens (`<!-- BADGES_START -->`) to rewrite header properties dynamically without affecting documentation content.

Automated pipelines layout config (`.github/workflows/ci.yml`):

```yaml
name: CI/CD Badge Automation Pipeline
on:
  push:
    branches: [ "main", "master" ]

jobs:
  quality-and-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Process Verification Pipelines
        run: |
          make install
          make lint
          make test
          
          # Compute contextual mapping tokens safely
          REPO_USER=$(echo "${{ github.repository }}" | cut -d'/' -f1)
          REPO_NAME=$(echo "${{ github.repository }}" | cut -d'/' -f2)
          
          # Safely inject centered properties
          ./badge_gen.sh flat-square top \
            "license" \
            "tech Python 3.12" \
            "metric repo-size $REPO_USER $REPO_NAME" \
            "build $REPO_USER $REPO_NAME"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Distribute Incremental Release Tags
        if: success() && github.ref == 'refs/heads/main'
        run: make tag

      - name: Commit & Push Updated Documentation
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: automated inline badges refresh [skip ci]"
          file_pattern: "README.md"
```

---

## 🔒 Security & Environment Auditing
To avoid leaking high-privilege access keys into public logging dashboards during pipeline validations, use the masked auditor routine:

```bash
make env-check
```
**Masked Safe Terminal Output Display:**
```text
🔒 Inspecting runtime variables securely...
--------------------------------------------------
GITHUB_TOKEN = ghp********123 (40 characters)
SNYK_TOKEN = snk********789 (36 characters)
WEBHOOK_URL = htt********com (33 characters)
--------------------------------------------------
```

---

## 🧹 Workspace Purging
Wipe local tracking clutter, temporary formatting assets, bytecode files, and compilation residues to maintain a clean project structure:
```bash
make clean
```

---

## 🧪 Testing Suite
The repository implements an enterprise-grade verification layout dividing validation jobs between code structure linting, isolated units mockups, and physical end-to-end integration tests.

```bash
# Automated Code Formatting Quality Verification
make lint

# Auto-resolve formatting variances via Black style standards
make commit-fix

# Run the 21 unit and integration test definitions
make test
```

### Mocking Strategy & Coverage Profile
The testing framework achieves **95%+ absolute code coverage**. Outgoing connections are managed using `requests_mock` fixtures to simulate network errors and verify text formatting boundaries without real network overhead. Local pre-commit Git hooks block staging actions automatically if the suite fails.

---

## 📜 License
MIT License — Check out the [LICENSE](LICENSE) asset for complete deployment and usage criteria.
