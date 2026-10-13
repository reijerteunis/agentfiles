#!/usr/bin/env bash
# Self-test for scripts/validate.py: builds a broken repo in a temp folder and checks that every
# mistake is caught. Fixtures are generated, not committed, so skill installers never discover them.
set -euo pipefail
cd "$(dirname "$0")/.."
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT

mkdir -p "$T/.claude-plugin" "$T/plugins/demo/.claude-plugin" "$T/plugins/unlisted"
echo '{"name":"fixture","owner":{"name":"Test"},"plugins":[{"name":"demo","source":"./plugins/demo"}]}' > "$T/.claude-plugin/marketplace.json"
echo '{"name":"demo"}' > "$T/plugins/demo/.claude-plugin/plugin.json"
skill() { mkdir -p "$T/plugins/demo/skills/$1"; printf '%s\n' "$2" > "$T/plugins/demo/skills/$1/SKILL.md"; }
skill wrong-name   $'---\nname: other-name\ndescription: Does a thing. Use it when testing.\n---\nBody'
skill bad-yaml     $'---\nname: bad-yaml\ndescription: Use when: this colon breaks YAML\n---\nBody'
skill extra-key    $'---\nname: extra-key\ndescription: Does a thing. Use it when testing.\nargument-hint: x\n---\nBody'
skill missing-ref  $'---\nname: missing-ref\ndescription: Does a thing. Use it when testing.\n---\nRead references/nope.md first.'
skill has-claude   $'---\nname: has-claude\ndescription: Does a thing. Use it when testing <b>bold</b>.\n---\nBody'

out="$(uv run scripts/validate.py --root "$T" 2>&1 || true)"
fail=0
expect() { if grep -q -- "$1" <<<"$out"; then echo " ✓ catches: $1"; else echo " ✗ missed:  $1"; fail=1; fi; }
expect "must equal the folder name"
expect "invalid YAML frontmatter"
expect "non-portable frontmatter keys"
expect "references missing file 'references/nope.md'"
expect "may not contain XML tags"
expect "not listed in .claude-plugin/marketplace.json"
expect "FAILED"
exit $fail
