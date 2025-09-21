import os, requests
from .base import PRAdapter

class GitHubAdapter(PRAdapter):
    def __init__(self):
        self.base = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")

    def _headers(self, accept="application/vnd.github.v3+json"):
        h = {"Accept": accept}
        if self.token:
            h["Authorization"] = f"token {self.token}"
        return h

    def get_pr_meta(self, repo, pr_id):
        r = requests.get(f"{self.base}/repos/{repo}/pulls/{pr_id}",
                         headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()

    def get_pr_diff(self, repo, pr_id):
        r = requests.get(f"{self.base}/repos/{repo}/pulls/{pr_id}",
                         headers=self._headers("application/vnd.github.v3.diff"),
                         timeout=30)
        r.raise_for_status()
        return r.text
