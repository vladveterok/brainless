# Universal Second Brain Ingester

An automated orchestration pipeline designed to capture unstructured data (text, URLs, YouTube videos) via Telegram, process it through an LLM for summarization and tagging, and persist it to your knowledge graph (Obsidian).

This repository is built with **n8n** and a custom **Python microservice** for extracting YouTube transcripts. It features a **Dual Environment Architecture**, meaning you can run it purely locally on your laptop, or deploy it headless to a 100% Free Cloud VPS.

## Prerequisites
Before choosing your deployment track, you will need three API keys:
1. **Telegram Bot Token**: Go to Telegram, message `@BotFather`, send `/newbot`, and copy the HTTP API Token.
2. **Gemini API Key**: Go to [Google AI Studio](https://aistudio.google.com/), sign in, and click **Create API Key**. This is 100% free and gives a massive 1-Million-token context window.
3. **GitHub Personal Access Token (For Cloud Track Only)**: Go to GitHub -> Settings -> Developer Settings -> Personal Access Tokens (Fine-grained). Create a token strictly scoped to your Vault repository with "Contents: Read and Write" permissions.

---

## Deployment Tracks
Choose the track that fits your workflow.

### Track A: Local Deployment (Mac/Windows/Linux)
*Best for: Users who want 100% local data control and want to write directly to their local Obsidian app.*

**1. Prepare Obsidian**
- Install the [Obsidian Local REST API Plugin](https://github.com/coddingtonbear/obsidian-local-rest-api) from the Community Plugins tab.
- Enable the plugin and copy your API Key.

**2. Configure the Environment**
- Run `./scripts/setup_host.sh` to generate the `.env` file.
- Start a local tunnel to expose port 5678 to the internet: `npx localtunnel --port 5678 --subdomain your-stable-name`
- Open `.env` and set:
  ```env
  STORAGE_MODE=local
  OBSIDIAN_API_KEY=your_obsidian_key_here
  WEBHOOK_URL=https://your-tunnel-url.loca.lt
  TELEGRAM_BOT_TOKEN=your_token
  GEMINI_API_KEY=your_token
  ```

**3. Run the Stack**
- Run `./scripts/setup_host.sh` again to start Docker Compose.
- Open `http://localhost:5678` in your browser.
- Import `workflows/main_workflow.json`.
- Double-click the Telegram Trigger node, select "Create New Credential", name it "My Telegram Bot", type `dummy` as the token (Docker handles the real token securely via `.env`), and activate the workflow.

---

### Track B: 100% Free Cloud Deployment (Google Cloud VPS)
*Best for: Users who want a headless bot running 24/7, even when their laptop is closed.*

For the complete, step-by-step tutorial on how to set up GitHub synchronization, deploy the engine to a free Google Cloud e2-micro instance, and configure the Obsidian Git plugin, please refer to the comprehensive [Google Cloud & GitHub Deployment Guide](DEPLOYMENT_GUIDE.md).

---

## How to Use
Send a message to your Telegram bot. 
- **Send an Article URL:** It extracts the full text, Gemini summarizes it with 5 key takeaways, tags it, and saves it.
- **Send a YouTube URL:** It bypasses YouTube protections, extracts the raw transcript, Gemini summarizes it, tags it, and saves it.
- **Send Text:** It parses your text, tags it, and saves it.
- **Custom Prompts:** You can append custom instructions after a URL (e.g., `https://youtube.com/watch... extract all book recommendations`). Gemini will ignore the default summary format and execute your exact prompt.
