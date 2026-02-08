---
name: git-push
description: Automates the git add, commit, and push process. Use this when the user wants to sync their progress to GitHub with professional commit messages.
---

# Git Sync Skill

This skill ensures a clean and descriptive commit history.

## Steps to Follow
1. **Stage Changes**: Execute `git add .` to capture all project files and skill updates.
2. **Generate Message**: Create a commit message following the "Conventional Commits" format.
   - Example: `feat: implement Groq-powered conflict resolution logic`
   - Example: `docs: update master implementation plan with tech requirements`
3. **Push**: Execute `git push origin main`.

## Safety Checks
- Verify that `.env` or API keys are listed in `.gitignore` before pushing.
- If a push fails due to a conflict, alert the user before attempting a pull.