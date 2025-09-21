import os, requests
from .base import PRAdapter

class GitLabAdapter(PRAdapter):
    def __init__(self):
        self.base = os.getenv("GITLAB_BASE", "https://gitlab.com/api/v4")
        self.token = os.getenv("GITLAB_TOKEN")

    def _headers(self, accept="application/json"):
        h = {"Accept": accept}
        if self.token:
            h["PRIVATE-TOKEN"] = self.token
        return h

    def get_pr_meta(self, repo, pr_id):
        # repo: numeric project ID OR URL-encoded path 'group%2Fproject'
        url = f"{self.base}/projects/{repo}/merge_requests/{pr_id}"
        r = requests.get(url, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()

    def get_pr_diff(self, repo, pr_id):
        url = f"{self.base}/projects/{repo}/merge_requests/{pr_id}/changes"
        r = requests.get(url, headers=self._headers(), timeout=30)
        r.raise_for_status()
        changes = r.json().get("changes", [])
        return "\n".join(c.get("diff", "") for c in changes if c.get("diff"))
