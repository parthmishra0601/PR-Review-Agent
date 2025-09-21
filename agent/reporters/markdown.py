# agent/reporters/markdown.py
def render(meta: dict, score: int, heur: list, linters: dict) -> str:
    parts = [
        "# PR Review Report",
        f"**Title:** {meta.get('title') or meta.get('description') or meta.get('body','')}",
        f"**Score:** {score}/100",
        "## Heuristic Findings",
    ]
    parts += [f"- {f}:{ln} — {msg}" for f,ln,msg in heur] or ["(none)"]
    parts += ["", "## Linter Summaries",
              "### flake8", linters.get("flake8") or "(none)",
              "### pylint", linters.get("pylint") or "(none)",
              "### bandit", linters.get("bandit") or "(none)"]
    return "\n".join(parts)
