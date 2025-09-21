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
🛠️ Tech Stack

Backend: Python 3.12, Flask

Linters: flake8, pylint, bandit

Diff Parser: unidiff

Deployment: Render

⚙️ Setup & Installation
1. Clone the repo
git clone https://github.com/YOUR-USER/PR-Review-Agent.git
cd PR-Review-Agent

2. Create & activate venv
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Set environment variables

Create a .env file (or export in shell):

GITHUB_TOKEN=ghp_xxxxxxx   # Needed to avoid GitHub API rate limits

5. Run locally
python main.py


Now open: http://127.0.0.1:8001

📂 Project Structure
agent/
 ├── adapters/        # GitHub, GitLab, Bitbucket adapters
 ├── analysis/        # diff_parser, rules, scorer, feedback
 ├── reporters/       # markdown report generator
templates/
 └── index.html       # Web UI template
main.py               # Flask app entrypoint
requirements.txt      # Python dependencies
README.md             # Documentation

🧪 Example Test PRs

GitHub: octocat/Hello-World PR 1

Flask repo: pallets/flask PR 5818

📦 Deployment (Render)

Push code to GitHub.

Connect repo to Render
.

Add environment variable in Render dashboard:

GITHUB_TOKEN = your GitHub PAT

Render will auto-build & deploy.

🙌 Acknowledgements

Built for #SRMHacksWithCodemate 🏆

Thanks to CodeMate for Build/Extension tools.

📌 Submission Links

🔗 Live App: https://pr-review-agent-4.onrender.com/

💻 GitHub Repo: https://github.com/YOUR-USER/PR-Review-Agent

📹 Demo Video: https://drive.google.com/file/d/1GUekso7CjTOZtbADuYVUaR5jClJcevlx/view?usp=sharing

🔖 LinkedIn Post: https://www.linkedin.com/posts/YOUR-POST

