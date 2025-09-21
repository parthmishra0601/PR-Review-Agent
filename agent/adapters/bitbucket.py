import os, base64, requests
from .base import PRAdapter

class BitbucketAdapter(PRAdapter):
    def __init__(self):
        self.base = "https://api.bitbucket.org/2.0"
        self.user = os.getenv("BITBUCKET_USER")
        self.app_pw = os.getenv("BITBUCKET_APP_PASSWORD")

    def _headers(self, accept="application/json"):
        h = {"Accept": accept}
        if self.user and self.app_pw:
            token = base64.b64encode(f"{self.user}:{self.app_pw}".encode()).decode()
            h["Authorization"] = f"Basic {token}"
        return h

    def get_pr_meta(self, repo, pr_id):
        # repo: 'workspace/repo-slug'
        url = f"{self.base}/repositories/{repo}/pullrequests/{pr_id}"
        r = requests.get(url, headers=self._headers(), timeout=30)
        r.raise_for_status()
        return r.json()

    def get_pr_diff(self, repo, pr_id):
        url = f"{self.base}/repositories/{repo}/pullrequests/{pr_id}/diff"
        r = requests.get(url, headers=self._headers("text/plain"), timeout=30)
        r.raise_for_status()
        return r.text  # unified diff
