# agent/adapters/base.py
from abc import ABC, abstractmethod

class PRAdapter(ABC):
    @abstractmethod
    def get_pr_meta(self, repo: str, pr_id: int):
        """Fetch PR/MR metadata (title, description, etc.)"""
        pass

    @abstractmethod
    def get_pr_diff(self, repo: str, pr_id: int):
        """Fetch PR/MR diff text"""
        pass
