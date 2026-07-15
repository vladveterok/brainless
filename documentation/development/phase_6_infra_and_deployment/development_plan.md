# Phase 6: Infrastructure & Deployment

**Status:** Done

## Objective
Finalize the deployment configuration so that the bot can be hosted 24/7 on a free cloud VPS (Google Cloud) while maintaining the ability to run locally. We will achieve this by implementing a "Dual Environment Architecture" in the n8n workflow and rewriting the README to act as a masterclass tutorial.

## Step-by-Step Plan
1. **Configuration Updates:** Update `.env.example` and `docker-compose.yml` to support the new `STORAGE_MODE` and GitHub API credentials. Explicitly pass variables into `N8N_ENV_VARS_ALLOW_LIST` to ensure n8n can read them.
2. **Workflow Routing:** Modify `main_workflow.json`:
   - Inject a `Switch` node right after the `Set Normalized Insights` node.
   - Branch A (`STORAGE_MODE=github`): Pushes Markdown to a GitHub repository using the GitHub API.
   - Branch B (`STORAGE_MODE=local`): Pushes Markdown to the local Obsidian instance via the Obsidian Local REST API.
   - Reconnect both branches to the `Telegram Send` node.
3. **README Overhaul:** Completely rewrite `README.md` to provide step-by-step instructions for both "Track A: Local Deployment" and "Track B: Cloud Deployment".

## Development History
* **2026-07-15**: Executed Dual Environment routing. Updated `docker-compose.yml` explicitly passing required secrets to avoid n8n access blockages. Overhauled README for Google Cloud Platform.
