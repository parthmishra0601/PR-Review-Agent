# agent/analysis/scorer.py

def score(linter_out: dict, heuristics: list) -> int:
    """
    Produce a simple 0–100 score.
    We penalize by the number of linter lines + heuristic findings (2 points each).
    """
    f8 = len(linter_out.get("flake8", "").strip().splitlines()) if linter_out.get("flake8") else 0
    py = len(linter_out.get("pylint", "").strip().splitlines()) if linter_out.get("pylint") else 0
    bd = len(linter_out.get("bandit", "").strip().splitlines()) if linter_out.get("bandit") else 0
    penalties = f8 + py + bd + len(heuristics)
    return max(100 - 2 * penalties, 0)
