# ==============================================================================
# 🛡️ Badge Gen - Shorthand Shortcuts Toolkit Compiler
# ==============================================================================

# Default visual style used across global quick calls
# Options: for-the-badge | flat | flat-square | plastic | social
STYLE = flat-square

.PHONY: help install lint test clean top config env-check commit-fix

help:
	@echo "🛡️  Badge Gen Toolkit Shorthand Shortcuts Menu:"
	@echo "--------------------------------------------------"
	@echo "  make install    - Install all dependencies and core engines"
	@echo "  make lint       - Run strict black & flake8 code style verifications"
	@echo "  make test       - Trigger the full automated 21-test suite with coverage"
	@echo "  make clean      - Complete purge of testing residue and runtime bytecode"
	@echo "  make config     - Interactively initialize access tokens (.env)"
	@echo "  make env-check  - Safely audit environment keys with masking protection"
	@echo "  make top        - Refresh and center core default badges into README header"
	@echo "  make commit-fix - Automatically format all code via Black to pass lint checks"
	@echo "--------------------------------------------------"

install:
	@chmod +x badge_gen.sh
	@./badge_gen.sh install

lint:
	@./badge_gen.sh lint

test:
	@./badge_gen.sh test

clean:
	@./badge_gen.sh clean

config:
	@./badge_gen.sh config

env-check:
	@./badge_gen.sh env-check

commit-fix:
	@if [ -f ".venv/bin/python3" ]; then \
		.venv/bin/python3 -m black . ; \
	elif [ -f "venv/bin/python3" ]; then \
		venv/bin/python3 -m black . ; \
	else \
		python3 -m black . ; \
	fi

top:
	@./badge_gen.sh $(STYLE) top "license" "tech Python 3.12" "tech Bash 5.2 4EAA25" "tech Open-Source Community success" "tech Maintained Yes blue" "tech Contributions welcome green"

tag:
	@echo "🏷️  Synchronizing tags with remote repository..."
	@git fetch --tags --force
	@echo "🏷️  Calculating next semantic version tag..."
	@LATEST_TAG=$$(git describe --tags --abbrev=0 2>/dev/null || echo "v1.0.0"); \
	echo "   Latest version found: $$LATEST_TAG"; \
	VERSION=$${LATEST_TAG#v}; \
	MAJOR=$$(echo $$VERSION | cut -d. -f1); \
	MINOR=$$(echo $$VERSION | cut -d. -f2); \
	PATCH=$$(echo $$VERSION | cut -d. -f3); \
	NEW_PATCH=$$(($$PATCH + 1)); \
	NEW_TAG="v$$MAJOR.$$MINOR.$$NEW_PATCH"; \
	echo "   Generating new dynamic tag: $$NEW_TAG"; \
	git tag $$NEW_TAG; \
	git push origin $$NEW_TAG