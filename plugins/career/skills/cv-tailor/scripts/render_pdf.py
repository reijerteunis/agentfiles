#!/usr/bin/env python3
"""Render a CV written in Markdown to an ATS-friendly PDF via headless Chrome. Standard library only.

Usage:
  python3 render_pdf.py cv.md cv.pdf            render (HTML comments such as evidence IDs are dropped)
  python3 render_pdf.py cv.md cv.html --html    write the HTML only
  python3 render_pdf.py --self-test

Supports the CV subset of Markdown: # name, ## section, ### role, - bullets, paragraphs, **bold**, [links](url).
Chrome is found at $CHROME, the macOS app paths, or google-chrome / chromium on PATH.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "cv.html"
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', text)


def md_to_html(md: str) -> tuple[str, str]:
    """Return (title, body html)."""
    md = COMMENT_RE.sub("", md)
    if md.startswith("---\n"):
        md = md.split("\n---", 1)[-1]
    out, in_list, title = [], False, "CV"
    for line in (raw.rstrip() for raw in md.splitlines()):
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        if bullet:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(bullet.group(1).strip())}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if not line.strip():
            continue
        for prefix, tag in (("### ", "h3"), ("## ", "h2"), ("# ", "h1")):
            if line.startswith(prefix):
                text = line[len(prefix):].strip()
                if tag == "h1":
                    title = text
                out.append(f"<{tag}>{inline(text)}</{tag}>")
                break
        else:
            out.append(f"<p>{inline(line.strip())}</p>")
    if in_list:
        out.append("</ul>")
    return title, "\n".join(out)


def find_chrome() -> str | None:
    candidates = [os.environ.get("CHROME"),
                  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    candidates += [shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")]
    return next((c for c in candidates if c and os.path.exists(c)), None)


def render(md_path: Path, out: Path, html_only: bool) -> int:
    title, body = md_to_html(md_path.read_text(encoding="utf-8"))
    page = TEMPLATE.read_text(encoding="utf-8").replace("{{title}}", html.escape(title)).replace("{{content}}", body)
    if html_only:
        out.write_text(page, encoding="utf-8")
        print(f"wrote {out}")
        return 0
    chrome = find_chrome()
    if not chrome:
        print("no Chrome or Chromium found: install one, set $CHROME, or use --html and print to PDF", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        page_path = Path(tmp) / "cv.html"
        page_path.write_text(page, encoding="utf-8")
        cmd = [chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={tmp}/profile",
               "--no-pdf-header-footer", "--print-to-pdf-no-header",
               f"--print-to-pdf={out.resolve()}", page_path.as_uri()]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0 or not out.exists():
        print(result.stderr[-2000:], file=sys.stderr)
        return 1
    print(f"wrote {out}")
    return 0


def self_test() -> int:
    title, body = md_to_html("# Jane Doe\njane@x.com · [site](https://x.com)\n## Experience\n"
                             "### Acme · Data Engineer · 2020 – 2024\n- Did **this** <!-- ac-1 -->\n- And that & more\n")
    checks = [title == "Jane Doe", "<h3>Acme · Data Engineer · 2020 – 2024</h3>" in body, "<strong>this</strong>" in body,
              "ac-1" not in body, "&amp; more" in body, '<a href="https://x.com">site</a>' in body,
              body.count("<ul>") == 1 and body.count("</ul>") == 1, TEMPLATE.exists()]
    print("render_pdf self-test:", "ok" if all(checks) else f"FAILED {checks}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a Markdown CV to PDF.")
    ap.add_argument("cv", nargs="?", type=Path)
    ap.add_argument("out", nargs="?", type=Path)
    ap.add_argument("--html", action="store_true", help="write HTML instead of PDF")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.cv and args.out):
        ap.error("give the Markdown CV and the output path")
    return render(args.cv, args.out, args.html)


if __name__ == "__main__":
    sys.exit(main())
