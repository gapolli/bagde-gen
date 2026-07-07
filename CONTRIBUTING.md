# 🤝 Contributing to Badge Gen

Thank you for your interest in improving **Badge Gen**! This project maintains a strict standard of clean code, high test coverage (96%+), and simple user experiences. 

Please read the guidelines below before opening a Pull Request.

## 📋 Table of Contents
- [Code of Conduct](#-code-of-conduct)
- [Development Workflow](#-development-workflow)
- [Testing Standards](#-testing-standards)
- [Commit Message Guidelines](#-commit-message-guidelines)
- [Pull Request Checklist](#-pull-request-checklist)

---

## 🏗️ Development Workflow

1. **Fork the Repository**: Create your own copy of the project.
2. **Create a Feature Branch**: Use descriptive names for your branches.
   ```bash
   git checkout -b feat/your-awesome-feature
   ```
3. **Set Up the Environment**: Install dependencies using the framework orchestrator.
   ```bash
   ./badge_gen.sh install
   ```
4. **Code with Architecture in Mind**: 
   - Keep `badge_gen.py` as a lightweight CLI engine.
   - Keep `badge_gen.sh` as a simplified wrapper interface for human developers and CI/CD routines.

---

## 🧪 Testing Standards

We do not merge Pull Requests that lower our current test coverage profile or break core functionalities.

- **Unit and Integration Execution**: Always run the automated testing pipeline before pushing changes.
  ```bash
  ./badge_gen.sh test
  ```
- **Network Requests Mocking**: If your feature introduces new network queries to Shields.io or external APIs, you **must use `requests_mock`** inside your test context. Do not make live network calls during test sweeps.
- **Environment Safety**: Test code that relies on tokens must intercept and clean target `.env` configurations safely using pytest fixtures.

---

## 📝 Commit Message Guidelines

We enforce semantic and clear commit formatting to automate release logs:
- `feat: ...` for a brand new functional capability.
- `fix: ...` for an isolated bug correction or logical regression.
- `docs: ...` for content modifications inside markdown files or help blocks.
- `test: ...` for adding or refactoring code coverage scenarios.

---

## 🚀 Pull Request Checklist

Before submitting your PR, double-check that you completed these milestones:
- [ ] Your code passes all tests local tests (`./badge_gen.sh test`).
- [ ] Code coverage has been maintained or improved.
- [ ] Documentation (`README.md`) has been updated if parameters changed.
- [ ] Branch commits follow the semantic layout.
