#!/usr/bin/env bash

# Internal default configurations
SCRIPT_PATH="badge_gen.py"
OUTPUT_DEFAULT="README.md"
STYLE_DEFAULT="for-the-badge"

# Terminal ANSI color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# --- AUTOMATIC PYTHON EXECUTABLE DETECTOR ---
# Dynamically resolves whether to use a local virtual environment or the global system Python
if [ "$CI" = "true" ] || [ -n "$GITHUB_ACTIONS" ]; then
    # 🚀 FIXED: In CI/CD pipelines, use the default active python command provided by actions/setup-python
    PY_EXEC="python"
elif [ -f ".venv/bin/python3" ]; then
    PY_EXEC=".venv/bin/python3"
elif [ -f "venv/bin/python3" ]; then
    PY_EXEC="venv/bin/python3"
else
    PY_EXEC="python3"
fi

# Detect CI/CD pipeline environment variables
if [ "$CI" = "true" ] || [ -n "$GITHUB_ACTIONS" ]; then
    IS_CI=true; NO_NOTIFY_FLAG="--no-notify"
else
    IS_CI=false; NO_NOTIFY_FLAG=""
fi

# --- DYNAMIC CLI VISUAL STYLE PARSING ---
if [[ "$1" =~ ^(for-the-badge|flat|flat-square|plastic|social)$ ]]; then
    STYLE_DEFAULT="$1"
    shift 
fi

COMMAND="$1"
shift

show_help() {
    cat << EOF
BADGE_GEN(1)                 User & CI/CD Manual                BADGE_GEN(1)

NAME
     badge_gen.sh - Simplified interface wrapper with dynamic style selection

SYNOPSIS
     ./badge_gen.sh [OPTIONAL_STYLE] [COMMAND] [OPTIONS]

VALID VISUAL STYLES
     for-the-badge | flat | flat-square | plastic | social

AVAILABLE PLUGINS / COMMANDS
     install         Validates the environment and installs pip requirements.
     test            Triggers the complete automated test suite with coverage.
     lint            Runs code quality and formatting checks (black & flake8).
     clean           Removes runtime testing cache files, coverage sweeps, and logs.
     top             Injects multiple centered badges into the README header.
     config          Initializes tokens and secure keys (.env) interactively.
     tech            Generates a static custom tech-stack brand badge.
     metric          Generates dynamic remote repository metrics from GitHub.
     build           Evaluates live execution status from GitHub Actions.
     sync            Bulk refreshes an entire markdown section via JSON.
     env-check       Safely inspects and masks local environment keys.

EOF
    exit 0
}

# --- INTERNAL ROUTINES ---
install_dependencies() {
    echo -e "${BLUE}📦 Verifying system environment and installing dependencies via ($PY_EXEC)...${NC}"
    $PY_EXEC -m pip install --upgrade pip
    $PY_EXEC -m pip install requests python-dotenv requests-mock pytest pytest-cov black flake8
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then $PY_EXEC -m pip install win10toast; fi
    echo -e "${GREEN}✅ Project dependencies successfully installed!${NC}"
}

run_lint() {
    echo -e "${BLUE}🧹 Running automated code quality checks (black & flake8) via ($PY_EXEC)...${NC}"
    local lint_failed=0

    echo -e "\n${BLUE}[1/2] Checking code formatting with Black...${NC}"
    if ! $PY_EXEC -m black --check . ; then
        echo -e "${YELLOW}⚠️ Formatting issues detected. You can fix them automatically by running: $PY_EXEC -m black .${NC}"
        lint_failed=1
    else
        echo -e "${GREEN}✨ Code formatting is perfectly compliant with Black standards!${NC}"
    fi

    echo -e "\n${BLUE}[2/2] Checking code style and syntax with Flake8...${NC}"
    if ! $PY_EXEC -m flake8 --max-line-length=120 --exclude=.venv,venv,env,tests ; then
        echo -e "${RED}❌ Code quality violations or syntax anomalies found by Flake8.${NC}"
        lint_failed=1
    else
        echo -e "${GREEN}✨ Code implementation style successfully passed Flake8 validation!${NC}"
    fi

    if [ $lint_failed -eq 1 ]; then
        exit 1
    fi
}

run_tests() {
    echo -e "${BLUE}🧪 Launching automated testing execution with coverage counters via ($PY_EXEC)...${NC}"
    PYTHONPATH=. $PY_EXEC -m pytest --cov=badge_gen tests/
}

add_to_top() {
    if [ ! -f "$OUTPUT_DEFAULT" ]; then touch "$OUTPUT_DEFAULT"; fi
    
    if ! grep -q "<!-- BADGES_START -->" "$OUTPUT_DEFAULT"; then
        echo -e "${BLUE}🔄 Injecting structural markdown anchors into $OUTPUT_DEFAULT...${NC}"
        local temp_init=$(mktemp)
        awk '/^[[:space:]]*#[[:space:]]+/ { print; print "<!-- BADGES_START -->\n<!-- BADGES_END -->"; next } { print }' "$OUTPUT_DEFAULT" > "$temp_init"
        if ! grep -q "<!-- BADGES_START -->" "$temp_init"; then
            echo -e "<!-- BADGES_START -->\n<!-- BADGES_END -->\n" > "$temp_init"
            cat "$OUTPUT_DEFAULT" >> "$temp_init"
        fi
        mv "$temp_init" "$OUTPUT_DEFAULT"
    fi

    local temp_badges=""
    echo -e "${BLUE}🛡️  Generating dynamic structural badges using '${STYLE_DEFAULT}' style...${NC}"

    for cmd_string in "$@"; do
        local single_badge
        single_badge=$(./badge_gen.sh "$STYLE_DEFAULT" $cmd_string 2>/dev/null | grep -E '^\[\!\[Badge\]|^\[\!\[|^\!\[Badge\]')
        if [ -n "$single_badge" ]; then temp_badges+="$single_badge "; fi
    done

    if [ -z "$temp_badges" ]; then 
        echo -e "${RED}❌ Validation Failure: No valid badges were generated from arguments.${NC}"
        exit 1
    fi
    
    temp_badges=$(echo "$temp_badges" | xargs)
    local center_block="<!-- BADGES_START -->\n<p align=\"center\">\n  ${temp_badges}\n</p>\n<!-- BADGES_END -->"

    local temp_file=$(mktemp)
    awk -v content="$center_block" '
    /<!-- BADGES_START -->/ { inside=1; print content; next } 
    /<!-- BADGES_END -->/ { inside=0; next } 
    !inside { print }
    ' "$OUTPUT_DEFAULT" > "$temp_file"
    mv "$temp_file" "$OUTPUT_DEFAULT"
    echo -e "${GREEN}🎉 Success! Header badges centered and synced without breaking the document structure.${NC}"
}

audit_environment() {
    local env_file=".env"
    if [ ! -f "$env_file" ]; then touch "$env_file"; fi
    echo -e "${BLUE}🔒 Inspecting runtime variables securely...${NC}"
    echo "--------------------------------------------------"
    while IFS= read -r line || [ -n "$line" ]; do
        if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then continue; fi
        local key="${line%%=*}"; local val="${line#*=}"
        val=$(echo "$val" | sed -E "s/^['\"]|['\"]$//g")
        local length=${#val}; local masked_val=""
        if [ $length -le 6 ]; then
            masked_val="****** (Value insecure / Too short)"
        else
            local first_three="${val:0:3}"; local last_three="${val: -3}"
            masked_val="${first_three}********${last_three} (${length} characters)"
        fi
        echo -e "${GREEN}${key}${NC} = ${YELLOW}${masked_val}${NC}"
    done < "$env_file"
    echo "--------------------------------------------------"
}

clean_cache() {
    echo -e "${BLUE}🧹 Initiating system purge of runtime testing cache directories and logs...${NC}"

    local targets=(
        ".pytest_cache"
        ".coverage"
        "htmlcov"
        "coverage.xml"
        ".mote"
        "badge_gen.egg-info"
    )
    
    local found=0

    for target in "${targets[@]}"; do
        if [ -e "$target" ]; then
            echo -e "   Removing asset: ${YELLOW}${target}${NC}"
            rm -rf "$target"
            found=1
        fi
    done

    if find . -type d -name "__pycache__" -print -quit | grep -q .; then
        echo -e "   Purging scattered Python bytecode cache segments... (${YELLOW}__pycache__${NC})"
        find . -type d -name "__pycache__" -exec rm -rf {} +
        found=1
    fi
    
    if [ $found -eq 1 ]; then
        echo -e "${GREEN}✨ Complete workspace decontamination accomplished successfully!${NC}"
    else
        echo -e "${GREEN}✨ Workspace is already pristine. No cache anomalies found.${NC}"
    fi
}

if [[ "$COMMAND" != "install" && "$COMMAND" != "test" && "$COMMAND" != "lint" && "$COMMAND" != "clean" && "$COMMAND" != "-h" && "$COMMAND" != "--help" && "$COMMAND" != "help" && "$COMMAND" != "env-check" && "$COMMAND" != "top" && "$COMMAND" != "" ]]; then
    if [ ! -f "$SCRIPT_PATH" ]; then 
        echo -e "${RED}❌ Core Error: Script engine '$SCRIPT_PATH' missing from root directory.${NC}"
        exit 1
    fi
fi

case "$COMMAND" in
    install)   install_dependencies ;;
    test)      run_tests ;;
    lint)      run_lint ;;
    clean)     clean_cache ;;
    config)    $PY_EXEC "$SCRIPT_PATH" setup ;;
    env-check) audit_environment ;;

    top)
        if [ "$#" -lt 1 ]; then
            echo -e "${RED}❌ Error: Please provide at least one badge definition string.${NC}"
            exit 1
        fi
        add_to_top "$@"
        ;;
    
    tech)
        LABEL="$1"; MSG="$2"; CUSTOM_COLOR="$3"
        if [ -z "$LABEL" ] || [ -z "$MSG" ]; then exit 1; fi
        LOGO=$(echo "$LABEL" | tr '[:upper:]' '[:lower:]')
        if [ -n "$CUSTOM_COLOR" ]; then
            $PY_EXEC "$SCRIPT_PATH" $NO_NOTIFY_FLAG static --label "$LABEL" --message "$MSG" --logo "$LOGO" --color "$CUSTOM_COLOR" --style "$STYLE_DEFAULT"
        else
            $PY_EXEC "$SCRIPT_PATH" $NO_NOTIFY_FLAG static --label "$LABEL" --message "$MSG" --logo "$LOGO" --style "$STYLE_DEFAULT"
        fi
        ;;
        
    metric)
        TYPE="$1"; USER="$2"; REPO="$3"
        if [ -z "$TYPE" ] || [ -z "$USER" ] || [ -z "$REPO" ]; then exit 1; fi
        $PY_EXEC "$SCRIPT_PATH" --hide-broken $NO_NOTIFY_FLAG dynamic --type "$TYPE" --user "$USER" --repo "$REPO" --style "$STYLE_DEFAULT"
        ;;
        
    build)
        USER="$1"; REPO="$2"
        if [ -z "$USER" ] || [ -z "$REPO" ]; then exit 1; fi
        $PY_EXEC "$SCRIPT_PATH" --hide-broken $NO_NOTIFY_FLAG dynamic --type "build-time" --user "$USER" --repo "$REPO" --style "$STYLE_DEFAULT"
        ;;
        
    sync)
        TITLE="$1"; FILE="$2"
        if [ -z "$TITLE" ] || [ -z "$FILE" ]; then exit 1; fi
        $PY_EXEC "$SCRIPT_PATH" --hide-broken $NO_NOTIFY_FLAG section --title "$TITLE" --file "$FILE" --output "$OUTPUT_DEFAULT"
        ;;
        
    -h|--help|help|"") show_help ;;
    *) echo -e "${RED}❌ Unknown target operation standard command '$COMMAND'.${NC}"; exit 1 ;;
esac
