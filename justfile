# agentfiles tasks. `just` lists them.

default:
    @just --list

# Static checks: skill spec, plugins, marketplace, evals, catalog, the README's guarantees, shell, secrets
validate:
    uv run scripts/validate.py --check-catalog
    bash scripts/test-validate.sh >/dev/null && echo "validator self-test ok"
    bash scripts/test-merge.sh
    python3 scripts/eval_report.py --self-test
    bash scripts/test-guarantees.sh
    @if command -v shellcheck >/dev/null; then shellcheck install.sh scripts/*.sh global/claude/statusline.sh && echo "shellcheck ok"; else echo "skip: shellcheck not installed"; fi
    @if command -v gitleaks >/dev/null; then gitleaks dir --no-banner --redact . && gitleaks git --no-banner --redact .; else echo "skip: gitleaks not installed"; fi
    @if command -v claude >/dev/null; then claude plugin validate .; else echo "skip: claude not installed"; fi

# Regenerate the skill catalog in README.md
catalog:
    uv run scripts/validate.py --write-catalog

# Scaffold a skill (and its plugin if it doesn't exist yet)
new plugin skill:
    scripts/new-skill.sh {{plugin}} {{skill}}

# Start Claude Code with a local plugin loaded, to try changes before pushing
try plugin:
    claude --plugin-dir plugins/{{plugin}}

# The README's guarantees, run on the planted problems in examples/, with their output
demo:
    @bash scripts/test-guarantees.sh --verbose

# Behavior evals with a no-plugin baseline. Real model calls: costs usage. Add --json result.json to publish.
eval plugin *args:
    claude plugin eval plugins/{{plugin}} {{args}}

# Publish eval scores (never the answers) from `just eval … --json` output, and refresh the README's results
eval-report *results:
    python3 scripts/eval_report.py import {{results}}

# Wire the repo into the AI tools on this machine (--dry-run, --check)
install *args:
    ./install.sh {{args}}
