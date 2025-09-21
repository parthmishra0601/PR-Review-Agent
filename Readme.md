# 🤖 PR Review Agent

An **AI-powered Pull Request Review Agent** built with **Python + Flask**, capable of analyzing PRs across multiple Git servers (GitHub, GitLab, Bitbucket).  
It fetches PR metadata & diffs, runs static analysis (**flake8**, **pylint**, **bandit**), applies heuristic checks (TODOs, bare excepts, secrets, print statements), and generates a **scored Markdown report** with actionable feedback.

---

## 🚀 Live Demo
- 🔗 **Deployed App:** [PR Review Agent](https://pr-review-agent-4.onrender.com/)  
- 📹 **Demo Video:** [Watch here](https://drive.google.com/file/d/1GUekso7CjTOZtbADuYVUaR5jClJcevlx/view?usp=sharing)  

---

## ✨ Features
- 🔄 **Multi-provider support**: GitHub (working), GitLab & Bitbucket (scaffolded).  
- 📊 **Code Quality Score**: PRs graded on a 0–100 scale.  
- 🔍 **Linters integrated**: flake8, pylint, bandit.  
- 🧩 **Heuristic checks**: Finds TODOs, bare excepts, print usage, possible secrets.  
- 📑 **Actionable feedback**: File:line-level suggestions for improvements.  
- 🌐 **Web UI**: Clean HTML form to enter repo + PR number.  

---

## 📸 Example Report
```markdown
# PR Review Report
**Title:** pass context through dispatch methods  
**Score:** 70/100  

## Heuristic Findings
(none)

## Feedback & Improvements
- src/flask/app.py:23 → Remove unused variable (flake8 F841)
- tests/test_reqctx.py:88 → Replace bare except with a specific exception
- bandit: subprocess call with shell=True → Avoid shell=True; pass args list to subprocess
