# agent/reporters/markdown.py
from agent.analysis.feedback import generate_feedback

def render(meta: dict, score: int, heur: list, linters: dict) -> str:
    """
    Build a Markdown report with heuristics, feedback, and linter summaries.
    """
    title = (
        meta.get("title")
        or meta.get("description")
        or meta.get("body", "")
        or "(no title)"
    )

    suggestions = generate_feedback(linters, heur)

    parts = [
        "# PR Review Report",
        f"**Title:** {title}",
        f"**Score:** {score}/100",
        "",
        "## Heuristic Findings",
    ]

    if heur:
        parts += [f"- {f}:{ln} — {msg}" for (f, ln, msg) in heur]
    else:
        parts.append("(none)")

    parts += [
        "",
        "## Feedback & Improvements",
    ]
    parts += [f"- {s}" for s in suggestions]

    parts += [
        "",
        "## Linter Summaries",
        "### flake8",
        linters.get("flake8") or "(none)",
        "",
        "### pylint",
        linters.get("pylint") or "(none)",
        "",
        "### bandit",
        linters.get("bandit") or "(none)",
    ]

    return "\n".join(parts)
