#!/usr/bin/env bash
# Regression test for scripts/merge-settings.jq: three layers, nested lists, local-only keys.
set -euo pipefail
cd "$(dirname "$0")/.."
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
echo '{"permissions":{"deny":["a","b"]},"hooks":{"SessionStart":[1]},"model":"local"}' > "$T/existing.json"
echo '{"permissions":{"deny":["b","c"]},"statusLine":{"type":"command"},"model":"repo"}' > "$T/base.json"
echo '{"permissions":{"deny":["d"]}}' > "$T/overlay.json"
out="$(jq -c -s -f scripts/merge-settings.jq "$T/existing.json" "$T/base.json" "$T/overlay.json")"
expected='{"permissions":{"deny":["a","b","c","d"]},"hooks":{"SessionStart":[1]},"model":"repo","statusLine":{"type":"command"}}'
if [[ "$(jq -S . <<<"$out")" == "$(jq -S . <<<"$expected")" ]]; then
  echo "settings merge test ok"
else
  echo "settings merge test FAILED"; echo " got:      $out"; echo " expected: $expected"; exit 1
fi
