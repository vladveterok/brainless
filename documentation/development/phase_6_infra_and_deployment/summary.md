# Phase 6 Summary: Infrastructure & Deployment

**Status:** Done

## What Was Accomplished
1. **Dual Environment Support (The "Smart" Workflow):**
   - We updated `main_workflow.json` to include an intelligent routing layer (Switch Node).
   - If `.env` contains `STORAGE_MODE=github`, the workflow automatically uploads the Markdown note directly to a specified GitHub repository via the GitHub REST API (encoding it in Base64 on the fly).
   - If `.env` contains `STORAGE_MODE=local`, it routes the note to the local Obsidian Vault.
2. **Environment Configurations:** Updated `docker-compose.yml` to explicitly inject the new variables into `N8N_ENV_VARS_ALLOW_LIST`, ensuring n8n can access the secrets without errors. Expanded `.env.example`.
3. **Masterclass Documentation:** The `README.md` was completely rewritten into a multi-track tutorial covering local deployment and Google Cloud Platform deployment.

## Code Impact
* `README.md`: Overhauled to include Local vs Cloud tracks.
* `.env.example`: Added `STORAGE_MODE`, `GITHUB_OWNER`, `GITHUB_REPO`, `GITHUB_TOKEN`.
* `docker-compose.yml`: Passed new env vars into the `n8n` container and explicitly added them to the allow-list.
* `workflows/main_workflow.json`: Refactored to include both `GitHub Storage Node` and `Obsidian Storage Node`, handled by a `Storage Router` switch.
