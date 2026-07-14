# Development Plan: Universal Second Brain Ingester

## Implementation Notes & Strict Constraints
*   **Infrastructure as Code:** Deploy n8n locally via Docker using a strict `docker-compose.yml` that mounts persistent volumes for n8n data to ensure enterprise-grade reliability.
*   **Secrets Management:** The rules strictly forbid hardcoding or putting secrets in `docker-compose.yml`. A robust `.env` file structure and a validation mechanism must be set up before spinning up n8n.
*   **Setup Scripts:** Create project-specific setup scripts (e.g., `./scripts/setup_host.sh`) rather than relying on manual commands.
*   **Obsidian Prerequisite:** Since the GUI Obsidian app or its plugins cannot be automated, the specific step in Phase 4 requires manual execution based on a provided guide.

## Phase 1: Environment Setup & Ingestion
**Goal:** Establish the n8n environment, connect the Telegram bot, and build the routing logic.
1.  Deploy n8n locally via Docker or on a free cloud service (e.g., Render, Railway).
2.  Create a new Telegram Bot via BotFather and secure the API Token.
3.  In n8n, configure the **Telegram Trigger** node to listen for incoming text messages.
4.  Implement a **Switch Node** using Regex expressions to branch the workflow into three paths: YouTube URLs, general HTTP URLs, and raw text.
5.  *Test:* Send a link and a text message to the bot to ensure the Switch node routes correctly.

## Phase 2: Extraction Integration
**Goal:** Successfully pull text payloads from links.
1.  **Web Articles:** Add an HTTP Request node to the Article branch. Set the URL to `https://r.jina.ai/{{$json.message.text}}`. Map the response (which will be clean Markdown) to a `raw_content` variable.
2.  **YouTube:** Add an HTTP Request node (or install an n8n community node) connecting to `youtube-transcript.io`. Pass the extracted Video ID to fetch the transcript and map it to `raw_content`.
3.  **Merge:** Bring all three branches (Text, Article, YouTube) back together into a single pipeline using a **Merge Node** (set to "Pass-through").

## Phase 3: AI Processing Integration
**Goal:** Transform raw extracted text into structured knowledge.
1.  Register for a free API key from Groq (or Google Gemini).
2.  Add an **Advanced AI / LLM Node** (or standard HTTP node pointing to the LLM API).
3.  Configure the System Prompt:
    *   *Prompt logic:* "You are an expert knowledge extractor. Read the provided text/transcript. Output a valid JSON object containing: a title, a 3-sentence summary, a list of 5 key takeaways, and a list of relevant tags (starting with #)."
4.  Feed the `raw_content` from Phase 2 into the LLM prompt.
5.  Add a **Set Node** to map the LLM's JSON response into the exact schema defined in the `Standardized Insight Object`.

## Phase 4: Building the Storage Adapter (Obsidian)
**Goal:** Persist the data via a modular connector.
1.  Create a **new, separate workflow** in n8n named `Adapter: Obsidian Storage`.
2.  Set its trigger to an **Execute Workflow Trigger** (this allows it to receive data from the main workflow).
3.  Install the "Local REST API" plugin inside your local Obsidian application and obtain the Bearer token.
4.  In the adapter workflow, use a markdown formatting node (or Code node) to structure the incoming JSON into a clean Markdown template (including YAML frontmatter for tags and source links).
5.  Add an HTTP Request node configured to `POST /vault/filepath.md` against your local Obsidian REST API IP/port.
6.  Return a success message back to the main workflow.

## Phase 5: Closing the Loop
**Goal:** Provide feedback to the user and finalize the repository.
1.  In the main workflow, after the Execute Workflow node completes, add a Telegram **Send Message** node.
2.  Format a success reply to the user: *"✅ Saved to Obsidian: [Title] with tags [Tags]"*.
3.  Export the main workflow and the adapter workflow as `main_workflow.json` and `adapter_obsidian.json`.
4.  Write a detailed `README.md` explaining how to import the JSON files into n8n and where to paste the required API keys.

## Phase 6: Infrastructure & Deployment
**Goal:** Establish a permanent, stable hosting and delivery pipeline.
1.  **Hosting Solution:** Define and implement a permanent hosting strategy for the n8n instance (replacing the temporary local docker setup if necessary).
2.  **Webhook Stability:** Replace the unstable `localtunnel` workaround with a production-grade reverse proxy (e.g., Cloudflare Tunnels, Nginx, or Caddy) to ensure reliable Telegram webhook delivery.