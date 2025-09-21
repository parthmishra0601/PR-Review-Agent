# agent/analysis/feedback.py
from typing import List, Dict

def _has(text: str, needle: str) -> bool:
    return needle in (text or "")

def generate_feedback(linters: Dict[str, str], heuristics: List[tuple]) -> List[str]:
    """
    Turn raw linter output + heuristics into actionable bullets.
    Returns a list of improvement suggestions (strings).
    """
    tips: List[str] = []
    f8 = linters.get("flake8", "") or ""
    py = linters.get("pylint", "") or ""
    bd = linters.get("bandit", "") or ""

    # Heuristic-driven suggestions
    if any("TODO" in m for _, _, m in heuristics):
        tips.append("Resolve or track TODO comments before merge (convert to issues if needed).")
    if any("Bare except" in m for _, _, m in heuristics):
        tips.append("Replace bare `except:` with specific exceptions and handle them explicitly.")
    if any("Use logging instead of print" in m for _, _, m in heuristics):
        tips.append("Replace `print()` with `logging` and configure log levels.")
    if any("Possible secret detected" in m for _, _, m in heuristics):
        tips.append("Remove any secrets from code; rotate keys and load via environment variables.")

    # flake8 patterns / style
    if _has(f8, "E9") or _has(f8, "FileNotFoundError"):
        tips.append("Run style/formatting locally with repo files present to get meaningful flake8 results.")
    if _has(f8, "E1") or _has(f8, "W1"):
        tips.append("Apply a formatter (Black) and run flake8 to fix whitespace/indentation issues.")
    if _has(f8, "F401") or "unused import" in f8.lower():
        tips.append("Remove unused imports (flake8 F401).")
    if _has(f8, "F841") or "assigned to but never used" in f8.lower():
        tips.append("Remove unused variables (flake8 F841).")

    # pylint patterns
    if "fatal" in py.lower() or "F0001" in py:
        tips.append("Pylint fatal errors indicate missing files or bad imports—run locally on a full checkout.")
    if "missing-module-docstring" in py or "missing-function-docstring" in py:
        tips.append("Add docstrings to modules/functions/classes to improve readability and lint scores.")
    if "consider-using-f-string" in py:
        tips.append("Use f-strings for cleaner, faster string formatting.")
    if "too-many-branches" in py or "too-many-locals" in py:
        tips.append("Refactor long/complex functions; extract helpers and reduce branching.")

    # bandit patterns / security
    if bd.strip():
        tips.append("Review Bandit findings and address any potential security issues flagged.")
    if "subprocess" in (f8 + py + bd).lower():
        tips.append("When using subprocess, prefer explicit argument lists and avoid shell=True unless necessary.")

    # Generic improvements if nothing else triggered
    if not tips:
        tips.append("Looks clean overall. Consider adding type hints and docstrings to maintain long-term quality.")
        tips.append("Add/expand tests for the changed areas and ensure CI runs flake8/pylint/bandit on PRs.")

    # De-duplicate while preserving order
    seen = set(); deduped = []
    for t in tips:
        if t not in seen:
            deduped.append(t); seen.add(t)
    return deduped
