#!/usr/bin/env bash
# The README's guarantees, checked: each one has to fail closed on the planted problems in examples/.
# `just validate` and CI run it; `just demo` runs it with --verbose to show what each check prints.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
verbose=false
[[ "${1:-}" == "--verbose" ]] && verbose=true
failed=0

check() {  # check <what it proves> <expected exit code> <expected text> -- <command...>
  local what=$1 want_code=$2 want_text=$3 out code
  shift 4
  out=$("$@" 2>&1)
  code=$?
  if $verbose; then printf '\n$ %s\n%s\n' "$*" "$out"; fi
  if [[ $code -eq $want_code && $out == *"$want_text"* ]]; then
    echo "ok: $what"
  else
    echo "FAILED: $what (exit $code, expected $want_code and \"$want_text\")"
    failed=1
  fi
}

# shellcheck disable=SC2317,SC2329  # called through check's "$@" (older shellcheck reports SC2317)
denied() {  # prints the deny rule if the shipped Claude Code settings contain it
  jq -er --arg rule "$1" '.permissions.deny[] | select(. == $rule)' global/claude/settings.json
}

# shellcheck disable=SC2317,SC2329  # called through check's "$@" (older shellcheck reports SC2317)
hook() {  # runs the guardrail hook on a Bash command, as Claude Code would
  printf '{"tool_input":{"command":"%s"}}' "$1" | sh plugins/agent-ops/skills/guardrail-design/assets/block-unsafe-git.sh
}

# 1. They draft; you send.
for tool in send_message reply forward; do
  check "email can't be sent: Gmail $tool is denied" 0 "$tool" -- denied "mcp__claude_ai_Gmail__$tool"
done
check "a commit that skips signing is blocked" 2 "Blocked" -- hook "git commit -m wip --no-gpg-sign"
check "a normal commit is allowed" 0 "" -- hook "git commit -m wip"

# 2. They cite; they don't invent.
check "a CV can't claim what the master CV doesn't say" 1 "numbers not in the cited source (bc-2): 12" -- \
  python3 plugins/career/skills/cv-tailor/scripts/check_claims.py examples/cv/tailored-cv.md examples/cv/master-cv.md
check "copy can't make a claim without proof" 1 "claim without proof: The fastest checkout" -- \
  python3 plugins/go-to-market/skills/messaging/scripts/proof_check.py examples/landing/page.md examples/landing/proof.md

# 3. Your context stays yours.
for rule in 'Read(**/.env)' 'Read(~/.ssh/**)' 'Read(~/.aws/**)'; do
  check "the file tools can't read secrets: $rule is denied" 0 "$rule" -- denied "$rule"
done

# 4. They prove they work.
check "the published eval results match their data" 0 "" -- python3 scripts/eval_report.py render --check

exit $failed
