#!/usr/bin/env bash
# Scaffold a skill (and its plugin, if new):  scripts/new-skill.sh <plugin> <skill-name>
set -euo pipefail
cd "$(dirname "$0")/.."
plugin=${1:?usage: scripts/new-skill.sh <plugin> <skill-name>}
name=${2:?usage: scripts/new-skill.sh <plugin> <skill-name>}
re='^[a-z0-9]+(-[a-z0-9]+)*$'
[[ $plugin =~ $re && $name =~ $re ]] || { echo "names must be kebab-case (a-z, 0-9, single hyphens)" >&2; exit 1; }
dir="plugins/$plugin/skills/$name"
[[ -e $dir ]] && { echo "$dir already exists" >&2; exit 1; }

if [[ ! -d plugins/$plugin ]]; then
  mkdir -p "plugins/$plugin/.claude-plugin" "plugins/$plugin/evals"
  jq --arg n "$plugin" '.name = $n' templates/plugin.json > "plugins/$plugin/.claude-plugin/plugin.json"
  jq --arg n "$plugin" '.plugins += [{"name": $n, "source": ("./plugins/" + $n), "description": "TODO: one sentence"}]' \
    .claude-plugin/marketplace.json > .claude-plugin/marketplace.json.tmp && mv .claude-plugin/marketplace.json.tmp .claude-plugin/marketplace.json
  echo "created plugin $plugin (fill in its description in plugin.json and marketplace.json)"
fi

mkdir -p "$dir"
sed "s/{{name}}/$name/g" templates/SKILL.md.tmpl > "$dir/SKILL.md"
echo "created $dir/SKILL.md"
echo "next: write it (docs/writing-skills.md), add evals in plugins/$plugin/evals/, then: just validate"
