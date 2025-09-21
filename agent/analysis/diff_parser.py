# agent/analysis/diff_parser.py
from io import StringIO
from unidiff import PatchSet

def parse_diff(diff_text: str):
    """
    Parse a unified diff string into a PatchSet and return:
      - patch: the PatchSet object
      - changed_py: sorted list of changed Python file paths (ending with .py)
    """
    patch = PatchSet(StringIO(diff_text))
    changed_py = sorted({f.path for f in patch if f.path.endswith(".py")})
    return patch, changed_py
