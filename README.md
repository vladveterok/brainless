# Universal Second Brain Ingester

An automated orchestration pipeline designed to capture unstructured data (text, URLs, YouTube videos) via Telegram, process it through an LLM for summarization and tagging, and persist it to your knowledge graph (Obsidian).

## Prerequisites
- Docker & Docker Compose
- Node.js (for `npx` localtunnel)
- Telegram account
- Google Account (for Gemini AI)

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

### 3. Obtain Google Gemini API Key
To process the extracted text (like long YouTube transcripts), we use the **Gemini 1.5 Flash** model because of its massive 1-Million-token free tier context window.
1. Go to [Google AI Studio](https://aistudio.google.com/) and sign in with your Google Account.
2. In the top-left menu, click **Get API Key**.
3. Click the **Create API Key** button.
4. Select a Google Cloud project (or let it create a new one for you).
5. Once generated, **copy the API Key**. (Keep this secret!)

### 4. Configure the Environment
1. In a new terminal, start a local tunnel to expose port 5678 to the internet. You can use the `--subdomain` flag to pick a stable URL:
   ```bash
   npx localtunnel --port 5678 --subdomain your-subdomain-name
   ```
2. Copy the `https://...loca.lt` URL it generates.
3. Open your `.env` file (in the root of this project) and set the following variables:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_token_here
   WEBHOOK_URL=https://your-tunnel-url.loca.lt
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### 5. Start the Services
Run the setup script again to validate your variables, build the custom Python microservice, and start the Docker stack:
```bash
./scripts/setup_host.sh
```
*Note: This spins up both `n8n` and the internal `youtube-extractor` microservice designed to bypass YouTube anti-bot protections.*

### 6. Setup n8n Workflow
1. Open `http://localhost:5678` in your browser and complete the initial n8n owner setup.
2. In n8n, click **Add workflow** -> **...** (top right menu) -> **Import from File**.
3. Select `workflows/main_workflow.json` from this repository.
4. **Configure Telegram:** Double-click the **Telegram Trigger** node, select **Create New Credential** under "Credential for Telegram API". Name it "My Telegram Bot", type `dummy` in the token field (it will automatically be overwritten securely by your `.env` file in the background), and save.
5. Toggle the workflow to **Active** (top right corner).
6. Send a YouTube video link or a web article to your Telegram bot to test the pipeline! You should see it execute in the n8n dashboard and process it via the Gemini AI node.
