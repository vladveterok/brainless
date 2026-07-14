# Universal Second Brain Ingester

An automated orchestration pipeline designed to capture unstructured data (text, URLs, YouTube videos) via Telegram, process it through an LLM for summarization and tagging, and persist it to your knowledge graph (Obsidian).

## Prerequisites
- Docker & Docker Compose
- Node.js (for `npx` localtunnel)
- Telegram account

## Quick Start Guide

### 1. Initialize Configuration
Run the setup script to generate your `.env` file:
```bash
./scripts/setup_host.sh
```
*(This will intentionally fail the validation check, but it provisions your `.env` file).*

### 2. Create your Telegram Bot
1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`, and follow the prompts to create a name and username.
3. BotFather will provide an **HTTP API Token**. Copy it.

### 3. Configure the Environment
1. In a new terminal, start a local tunnel to expose port 5678 to the internet, you can use --subdomain flag and provide teh subdomain from WEBHOOK_URL in .env:§
   ```bash
   npx localtunnel --port 5678 --subdomain your-subdomain 
   ```
2. Copy the `https://...loca.lt` URL it generates.
3. Open your `.env` file and set the following variables:
   ```env
   TELEGRAM_BOT_TOKEN=your_token_here
   WEBHOOK_URL=https://your-tunnel-url.loca.lt
   ```

### 4. Start the Service
Run the setup script again to validate your variables, pull the Docker image, and start the n8n container:
```bash
./scripts/setup_host.sh
```

### 5. Setup n8n
1. Open `http://localhost:5678` in your browser and complete the initial n8n owner setup.
2. In n8n, click `Add workflow` -> `...` (top right menu) -> `Import from File`.
3. Select `workflows/main_workflow.json` from this repository.
4. Double-click the **Telegram Trigger** node, select **Create New Credential** under "Credential for Telegram API".
5. Name it "My Telegram Bot", type "dummy" in the token field (it will automatically be overwritten securely by your `.env` file in the background), and save.
6. Click **Execute workflow** and send a message to your Telegram bot to verify the connection.
