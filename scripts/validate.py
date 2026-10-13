#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Validate the repo: marketplace, plugins, skills, evals, global instructions and the README catalog.

Skills are checked against the Agent Skills spec (agentskills.io) plus this repo's standard
(docs/writing-skills.md), so they load in claude.ai, Claude Code, Codex and every other tool.

Usage:
  uv run scripts/validate.py [--root DIR]      check everything, exit 1 on errors
  uv run scripts/validate.py --check-catalog   also fail if the README catalog is out of date
  uv run scripts/validate.py --write-catalog   regenerate the README catalog
  uv run scripts/validate.py --root ../agentfiles-private --vendored third-party
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
XML_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")
LOCAL_REF_RE = re.compile(r"(?<![\w/.-])((?:references|scripts|assets)/[\w./-]*\w)")
RESERVED_PLUGIN_PREFIXES = ("claude-", "anthropic-", "anthropics-", "cc-plugin-")
RESERVED_PLUGIN_NAMES = {"claude", "anthropic", "claude-code", "claude-mods"}
PROMPT_KEYS = {"schema_version", "name", "description", "tags", "plugins", "runs", "expected_outcome",
               "model", "max_turns", "timeout_seconds", "allowed_tools", "append_system_prompt", "env"}
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}
MAX_SKILL_LINES = 500
MAX_GLOBAL_CHARS = 6000  # the tightest global-instruction limit among supported tools (Devin)
CATALOG_START, CATALOG_END = "<!-- catalog:start -->", "<!-- catalog:end -->"


class Report:
    def __init__(self, root: Path, vendored: set[str] | None = None) -> None:
        self.root, self.errors, self.warnings = root, [], []
        self.vendored = vendored or set()

    def error(self, path: Path, msg: str) -> None:
        rel = path.relative_to(self.root)
        # Vendored plugins hold other people's skills, kept verbatim: report, but don't fail on them
        if len(rel.parts) > 1 and rel.parts[0] == "plugins" and rel.parts[1] in self.vendored:
            self.warnings.append(f"{rel}: (vendored) {msg}")
        else:
            self.errors.append(f"{rel}: {msg}")

    def warn(self, path: Path, msg: str) -> None:
        self.warnings.append(f"{path.relative_to(self.root)}: {msg}")


def frontmatter(path: Path, report: Report) -> tuple[dict | None, str]:
    """Return (frontmatter mapping, body). Reports and returns None when the YAML is missing or invalid."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        report.error(path, "missing YAML frontmatter (file must start with ---)")
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        report.error(path, "frontmatter is not closed with ---")
        return None, text
    raw, body = text[4:end], text[end + 4:].lstrip("\n")
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        # The classic cause: an unquoted ": " inside a value. Tools then load the skill with empty
        # metadata and it silently never triggers.
        report.error(path, f"invalid YAML frontmatter ({exc.__class__.__name__}): quote values that contain ': '")
        return None, body
    if not isinstance(data, dict):
        report.error(path, "frontmatter must be a mapping")
        return None, body
    return data, body


def check_skill(skill_dir: Path, report: Report) -> dict | None:
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        report.error(skill_dir, "skill folder without SKILL.md")
        return None
    meta, body = frontmatter(path, report)
    if meta is None:
        return None

    unknown = set(meta) - SKILL_KEYS
    if unknown:
        report.error(path, f"non-portable frontmatter keys {sorted(unknown)}: only {sorted(SKILL_KEYS)} "
                           "load everywhere (claude.ai and the Skills API reject the rest)")

    name = meta.get("name")
    if not isinstance(name, str) or not name:
        report.error(path, "name is required")
    else:
        if name != skill_dir.name:
            report.error(path, f"name '{name}' must equal the folder name '{skill_dir.name}'")
        if not NAME_RE.match(name) or len(name) > 64:
            report.error(path, "name must be 1-64 chars of a-z, 0-9 and single hyphens")
        if "anthropic" in name or "claude" in name:
            report.error(path, "name may not contain 'anthropic' or 'claude'")

    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        report.error(path, "description is required")
    else:
        if len(desc) > 1024:
            report.error(path, f"description is {len(desc)} chars (max 1024)")
        if XML_TAG_RE.search(desc):
            report.error(path, "description may not contain XML tags")
        if "use" not in desc.lower():
            report.warn(path, "description should say when to use the skill ('Use it when…')")

    if "compatibility" in meta and (not isinstance(meta["compatibility"], str) or len(meta["compatibility"]) > 500):
        report.error(path, "compatibility must be a string of at most 500 chars")
    if "metadata" in meta and not (isinstance(meta["metadata"], dict)
                                   and all(isinstance(k, str) and isinstance(v, str) for k, v in meta["metadata"].items())):
        report.error(path, "metadata must map strings to strings (quote numbers: version: \"1.0\")")

    lines = path.read_text(encoding="utf-8").count("\n") + 1
    if lines > MAX_SKILL_LINES:
        report.error(path, f"{lines} lines (max {MAX_SKILL_LINES}): move detail into references/")

    # Every file the skill points at must exist inside the skill folder (single-skill installs copy only it)
    for ref in sorted(set(LOCAL_REF_RE.findall(body))):
        if not (skill_dir / ref).exists():
            report.error(path, f"references missing file '{ref}'")
    for f in skill_dir.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".py", ".sh", ".html", ".json", ".yaml", ".yml", ".toml"}:
            if re.search(r"/Users/[A-Za-z]|/home/[a-z]", f.read_text(encoding="utf-8", errors="ignore")):
                report.error(f, "contains an absolute home path; skills must be portable")
    return {"name": name, "description": desc or ""}


def check_evals(plugin_dir: Path, report: Report) -> int:
    cases = 0
    evals = plugin_dir / "evals"
    if not evals.is_dir():
        report.warn(plugin_dir, "no evals/ suite (see docs/writing-skills.md)")
        return 0
    for case in sorted(p for p in evals.rglob("*") if p.is_dir() and (p / "prompt.md").exists()):
        cases += 1
        meta, body = frontmatter(case / "prompt.md", report)
        if meta is not None:
            unknown = set(meta) - PROMPT_KEYS
            if unknown:
                report.error(case / "prompt.md", f"unknown keys {sorted(unknown)} (claude plugin eval rejects them)")
            if not body.strip():
                report.error(case / "prompt.md", "empty prompt")
        graders = sorted((case / "graders").glob("*.md"))
        if not graders:
            report.error(case, "eval case without graders/")
        for g in graders:
            gmeta, _ = frontmatter(g, report)
            if gmeta is not None and gmeta.get("type") not in GRADER_TYPES:
                report.error(g, f"type must be one of {sorted(GRADER_TYPES)}")
    if cases == 0:
        report.warn(evals, "no eval cases yet: add a trigger case and a near-miss (docs/writing-skills.md)")
    return cases


def check_agents(plugin_dir: Path, report: Report) -> int:
    """Subagents (agents/*.md) need a name and a description; Claude Code and Cowork load them."""
    agents = sorted((plugin_dir / "agents").glob("*.md"))
    for path in agents:
        meta, body = frontmatter(path, report)
        if meta is None:
            continue
        name = meta.get("name")
        if not isinstance(name, str) or not NAME_RE.match(name):
            report.error(path, "agent name is required and must be kebab-case")
        if not isinstance(meta.get("description"), str) or not meta["description"].strip():
            report.error(path, "agent description is required (it decides when the agent is used)")
        if not body.strip():
            report.error(path, "agent has no instructions")
    return len(agents)


def run_self_tests(skill_dir: Path, report: Report) -> int:
    """Bundled scripts that support --self-test must pass it: they are code the agent will run."""
    ran = 0
    for script in sorted((skill_dir / "scripts").glob("*.py")):
        if "--self-test" not in script.read_text(encoding="utf-8", errors="ignore"):
            continue
        ran += 1
        result = subprocess.run([sys.executable, str(script), "--self-test"], capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            report.error(script, f"--self-test failed: {(result.stdout + result.stderr).strip()[-300:]}")
    return ran


def check_marketplace(root: Path, report: Report) -> list[dict]:
    path = root / ".claude-plugin" / "marketplace.json"
    if not path.is_file():
        report.error(root, "missing .claude-plugin/marketplace.json")
        return []
    try:
        market = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(path, f"invalid JSON: {exc}")
        return []
    if not NAME_RE.match(str(market.get("name", ""))):
        report.error(path, "marketplace name must be kebab-case")
    if not (market.get("owner") or {}).get("name"):
        report.error(path, "owner.name is required")

    entries = market.get("plugins") or []
    listed = set()
    for entry in entries:
        name, source = entry.get("name", ""), entry.get("source", "")
        listed.add(name)
        if not NAME_RE.match(name) or name.startswith(RESERVED_PLUGIN_PREFIXES) or name in RESERVED_PLUGIN_NAMES:
            report.error(path, f"plugin name '{name}' is not kebab-case or is reserved")
        if not isinstance(source, str) or not source.startswith("./") or ".." in source:
            report.error(path, f"plugin '{name}': source must be a ./relative path inside the repo")
            continue
        manifest = root / source / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            report.error(path, f"plugin '{name}': {source}/.claude-plugin/plugin.json not found")
            continue
        try:
            plugin = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(manifest, f"invalid JSON: {exc}")
            continue
        if plugin.get("name") != name:
            report.error(manifest, f"name '{plugin.get('name')}' differs from the marketplace entry '{name}'")
        if "version" in plugin or "version" in entry:
            report.warn(manifest, "a version pins installs: bump it on every release, or omit it to track commits")
    for d in sorted((root / "plugins").glob("*/")):
        if d.name not in listed:
            report.error(d, "plugin folder is not listed in .claude-plugin/marketplace.json")
    return entries


def catalog(root: Path, entries: list[dict], skills: dict[str, list[dict]]) -> str:
    rows = ["| Plugin | Skill | What it does |", "|---|---|---|"]
    for entry in entries:
        for skill in skills.get(entry["name"], []):
            first = re.split(r"(?<=[.!?])\s", skill["description"].strip(), maxsplit=1)[0]
            path = f"{entry['source'][2:]}/skills/{skill['name']}/SKILL.md"
            rows.append(f"| `{entry['name']}` | [`{skill['name']}`]({path}) | {first} |")
    return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--check-catalog", action="store_true")
    ap.add_argument("--write-catalog", action="store_true")
    ap.add_argument("--vendored", action="append", default=[], metavar="PLUGIN",
                    help="plugin holding third-party skills kept verbatim: report its problems as warnings")
    args = ap.parse_args()
    root = args.root.resolve()
    report = Report(root, set(args.vendored))

    entries = check_marketplace(root, report)
    skills: dict[str, list[dict]] = {}
    n_skills = n_cases = n_agents = n_tests = 0
    for entry in entries:
        plugin_dir = root / entry.get("source", "")
        for skill_dir in sorted(p for p in (plugin_dir / "skills").glob("*") if p.is_dir()):
            info = check_skill(skill_dir, report)
            n_skills += 1
            n_tests += run_self_tests(skill_dir, report)
            if info:
                skills.setdefault(entry["name"], []).append(info)
        n_cases += check_evals(plugin_dir, report)
        n_agents += check_agents(plugin_dir, report)

    names = [s["name"] for group in skills.values() for s in group]
    for dup in sorted({n for n in names if names.count(n) > 1}):
        report.error(root, f"skill name '{dup}' is used twice (~/.agents/skills is one flat folder)")

    global_md = root / "global" / "AGENTS.md"
    if global_md.is_file() and len(global_md.read_text(encoding="utf-8")) > MAX_GLOBAL_CHARS:
        report.error(global_md, f"over {MAX_GLOBAL_CHARS} chars: some tools truncate global instructions")
    for f in root.rglob("*.json"):
        if ".git" in f.parts or "results" in f.parts:
            continue
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(f, f"invalid JSON: {exc}")

    readme = root / "README.md"
    if (args.check_catalog or args.write_catalog) and readme.is_file():
        text = readme.read_text(encoding="utf-8")
        if CATALOG_START in text and CATALOG_END in text:
            head, rest = text.split(CATALOG_START, 1)
            _, tail = rest.split(CATALOG_END, 1)
            fresh = f"{head}{CATALOG_START}\n{catalog(root, entries, skills)}\n{CATALOG_END}{tail}"
            if args.write_catalog and fresh != text:
                readme.write_text(fresh, encoding="utf-8")
                print("README catalog updated")
            elif args.check_catalog and fresh != text:
                report.error(readme, "skill catalog is out of date: run `just catalog`")
        else:
            report.error(readme, f"missing {CATALOG_START} / {CATALOG_END} markers")

    for w in report.warnings:
        print(f"warning: {w}")
    for e in report.errors:
        print(f"error:   {e}")
    status = "FAILED" if report.errors else "ok"
    print(f"{status}: {len(entries)} plugins, {n_skills} skills, {n_agents} agents, {n_cases} eval cases, "
          f"{n_tests} script self-tests, {len(report.errors)} errors, {len(report.warnings)} warnings")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
