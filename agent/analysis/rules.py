# agent/analysis/rules.py
import os, sys, subprocess, re

def _run_tool(module, args):
    """Run a Python module (flake8/pylint/bandit) inside the current venv."""
    r = subprocess.run([sys.executable, "-m", module, *args],
                       capture_output=True, text=True, env=os.environ.copy())
    return (r.stdout or "") + (("\n"+r.stderr) if r.stderr else "")

def run_linters(py_paths):
    """
    Returns dict with outputs from flake8, pylint, bandit for given Python file paths.
    If py_paths is empty, returns empty outputs.
    """
    out = {"flake8": "", "pylint": "", "bandit": ""}
    if py_paths:
        out["flake8"] = _run_tool("flake8", py_paths)
        out["pylint"] = _run_tool("pylint", py_paths)
        out["bandit"] = _run_tool("bandit", ["-q", "-r", *py_paths, "-f", "txt"])
    return out

def heuristic_checks(patch):
    """
    Lightweight heuristics on the unified diff PatchSet:
      - TODO comments
      - bare 'except:'
      - stray print() (except under tests/)
      - simple secret patterns (AWS Access Key, Google API key)
    Returns a list of tuples: (file_path, line_no, message)
    """
    findings = []
    secret_re = re.compile(r"(AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35})")
    for f in patch:
        for h in f:
            for l in h:
                if l.is_added:
                    t = l.value.strip()
                    if "TODO" in t:
                        findings.append((f.path, l.target_line_no, "TODO present"))
                    if t.startswith("except:"):
                        findings.append((f.path, l.target_line_no, "Bare except—catch specific exceptions"))
                    if "print(" in t and "/tests/" not in f.path:
                        findings.append((f.path, l.target_line_no, "Use logging instead of print"))
                    if secret_re.search(t):
                        findings.append((f.path, l.target_line_no, "Possible secret detected"))
    return findings
