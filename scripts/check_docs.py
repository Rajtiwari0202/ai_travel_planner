from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def iter_markdown_files() -> list[Path]:
    return sorted([*ROOT.glob("*.md"), *ROOT.glob("docs/**/*.md"), *ROOT.glob("research/**/*.md")])


def check_links() -> list[str]:
    errors: list[str] = []
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("F:"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path}: broken link: {target}")
    return errors


def check_diagrams() -> list[str]:
    errors: list[str] = []
    source = ROOT / "docs" / "architecture" / "diagrams" / "source"
    rendered = ROOT / "docs" / "architecture" / "diagrams" / "rendered"
    sources = sorted(source.glob("*.mmd"))
    if len(sources) != 18:
        errors.append(f"expected 18 Mermaid sources, found {len(sources)}")
    for item in sources:
        base = item.stem
        for suffix in ("svg", "png"):
            output = rendered / f"{base}.{suffix}"
            if not output.exists() or output.stat().st_size == 0:
                errors.append(f"missing rendered diagram: {output.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = [*check_links(), *check_diagrams()]
    if errors:
        print("\n".join(errors))
        return 1
    print("docs=ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
