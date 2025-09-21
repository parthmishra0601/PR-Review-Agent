from flask import Flask, render_template, request
import os, sys, requests

# ensure project root on path
sys.path.insert(0, os.path.dirname(__file__))

# import all three adapters
from agent.adapters.github import GitHubAdapter
from agent.adapters.gitlab import GitLabAdapter
from agent.adapters.bitbucket import BitbucketAdapter

from agent.analysis.diff_parser import parse_diff
from agent.analysis.rules import run_linters, heuristic_checks
from agent.analysis.scorer import score
from agent.reporters.markdown import render as render_md

app = Flask(__name__)

# register adapters for all providers
ADAPTERS = {
    "github": GitHubAdapter,
    "gitlab": GitLabAdapter,
    "bitbucket": BitbucketAdapter,
}

@app.route("/", methods=["GET","POST"])
def index():
    feedback, error = "", ""
    if request.method == "POST":
        provider = request.form.get("provider","github").strip().lower()
        repo     = request.form.get("repo","").strip()
        pr       = request.form.get("pr","").strip()

        if provider not in ADAPTERS:
            error = f"Unsupported provider: {provider}"
        elif not repo or not pr.isdigit():
            error = "Enter repo as 'owner/name' (or GitLab project id/encoded path) and a numeric PR/MR."
        else:
            try:
                adapter = ADAPTERS[provider]()
                meta = adapter.get_pr_meta(repo, int(pr))
                diff = adapter.get_pr_diff(repo, int(pr))
                patch, changed_py = parse_diff(diff)
                linters = run_linters(changed_py)
                heur = heuristic_checks(patch)
                s = score(linters, heur)
                feedback = render_md(meta, s, heur, linters)
            except requests.HTTPError as e:
                error = f"{provider} API error: {e.response.status_code} {e.response.text[:300]}"
            except Exception as e:
                error = f"Error: {e}"

    return render_template("index.html", feedback=feedback, error=error)

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port, debug=False)

