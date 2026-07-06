# 🛡️ Badge Gen

A Command Line Interface (CLI) designed to automate the generation of dynamic and static badges for GitHub documentation.

## 📋 Table of Contents
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Environment Configuration](#-environment-configuration)
- [Usage Guide](#-usage-guide)
- [CI/CD Automation](#-cicd-automation)
- [Testing](#-testing)

## 📋 Prerequisites
- Python 3.8 or higher.
- A GitHub Personal Access Token (for repository metrics).
- (Optional) Snyk API Token for security metrics.
- (Optional) UptimeRobot API Key for latency monitoring.

## 🚀 Installation
Clone this repository and install the required dependencies:
```bash
pip install requests python-dotenv requests-mock pytest pytest-cov win10toast
```

## ⚙️ Environment Configuration
Initialize your environment variables securely:
```bash
python badge_gen.py setup
```
This command will prompt you for your API tokens and Webhook URLs, saving them into a `.env` file.

## 💡 Usage Guide

### 1. Static Badges (Technology Stack)
Static badges use pre-defined color mapping for official brand recognition.
```bash
python badge_gen.py static --label "Python" --message "3.12" --logo "python"
```

### 2. Dynamic Performance Badges
Monitor real-time metrics such as build duration and API latency.
```bash
# Build Duration from GitHub Actions
python badge_gen.py dynamic --type build-time --user "user" --repo "repo" --workflow "main.yml"

# API Response Time (Latency)
python badge_gen.py dynamic --type response-time --uptime-key "monitor-key"
```

### 3. Repository Visibility Filter
The `--hide-broken` flag prevents "unknown" or "error" badges from appearing in your README.
```bash
python badge_gen.py --hide-broken dynamic --type actions --user "user" --repo "repo" --workflow "ci.yml"
```

## 🤖 CI/CD Automation (GitHub Actions)
Integrate badge updates into your deployment pipeline. Example workflow:
```yaml
name: Documentation Sync
on: [push]
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update Section
        run: python badge_gen.py --no-notify section --title "Metrics" --file stats.json --output README.md
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}
          WEBHOOK_URL: \${{ secrets.WEBHOOK_URL }}
```

## 🧪 Testing
The project includes a robust test suite using mocks to validate logic without external network dependencies.
```bash
pytest --cov=badge_gen tests/
```

## Sample Badges
![Badge](https://shields.ioPython-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
## License
MIT
