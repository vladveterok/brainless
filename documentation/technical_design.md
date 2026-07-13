# Technical Design Document (TDD): Universal Second Brain Ingester

## 1. System Overview
The Universal Second Brain Ingester is an automated orchestration pipeline designed to capture unstructured data (text, URLs, YouTube videos) via a messaging interface, extract the core content, process it through a Large Language Model (LLM) for summarization and tagging, and persist it to a local or cloud-based knowledge graph.

The system emphasizes a modular, zero-cost architecture utilizing free-tier APIs and open-source orchestration.

## 2. Architecture & Data Flow

The architecture is divided into three distinct decoupled layers:
1. **Ingestion & Routing:** Captures user input and determines the processing path.
2. **Extraction & Processing:** Fetches raw data and transforms it into structured insights using AI.
3. **Storage Adapter (Sub-Workflow):** Normalizes the payload and pushes it to the target database.

### Flow Diagram
[Telegram Bot] -> (Webhook) -> [Router Node]
                                  ├──> (Raw Text) ------------------------> [AI Summarizer]
                                  ├──> (Article URL) -> [Jina AI Reader] -> [AI Summarizer]
                                  └──> (YouTube URL) -> [YT Transcript] --> [AI Summarizer]
                                                                                  │
                                                                           [Set Normalized JSON]
                                                                                  │
                                                            [Execute Sub-Workflow (Storage Adapter)]
                                                                                  │
                                                                          [Obsidian REST API]
## 3. Component Breakdown

### 3.1 Orchestration Platform
*   **n8n (Self-hosted or Free Tier):** Acts as the central nervous system. N8n's visual node-based execution and native support for Sub-Workflows make it ideal for the adapter pattern.

### 3.2 Ingestion Layer
*   **Telegram Trigger Node:** Listens for new messages sent to a dedicated Telegram Bot.
*   **Switch Node (Router):** Uses regex to classify the incoming message string:
    *   `^https?://.*youtube\.com/|^https?://youtu\.be/` -> YouTube Route
    *   `^https?://.*` -> Web Article Route
    *   `Default` -> Raw Text Route

### 3.3 Extraction Layer
*   **YouTube Route:** Uses the free `youtube-transcript.io` API (via an HTTP Request node) or the `n8n-nodes-obsidian` community node to extract full video transcripts without requiring a YouTube Data API quota.
*   **Web Article Route:** Uses **Jina AI Reader API** (`https://r.jina.ai/{URL}`). This is a free endpoint that natively strips ads/menus and returns clean Markdown.

### 3.4 AI Processing Layer
*   **LLM Provider:** **Groq** (using `Llama-3-70b` or `Mixtral`) or **Google Gemini API**. Both offer generous free tiers. Groq is preferred for its sub-second inference speeds.
*   **System Prompt:** Instructs the LLM to process the raw input and output a strict JSON structure containing `summary`, `key_takeaways`, and `tags`.

### 3.5 Storage Adapter Layer (The Connector)
To support multiple storages, the main workflow ends at a "Set" node that standardizes the payload into the `Standardized Insight Object`. It then passes this object to an `Execute Workflow` node.
*   **Obsidian (Primary):** The Obsidian sub-workflow uses an HTTP Request node to send a `POST` request to the **Obsidian Local REST API** plugin (which runs locally on the user's machine), creating a new `.md` file in the vault.
*   **Future Adapters:** Notion, Roam, Logseq, or GitHub repos can be added as separate sub-workflows that accept the exact same Standardized Insight Object.

## 4. Data Schema

### Standardized Insight Object
This payload is the contract between the Processing Layer and the Storage Adapter.
```json
{
  "source_type": "youtube | article | text",
  "original_url": "string (nullable)",
  "title": "string",
  "generated_summary": "string",
  "takeaways": ["string"],
  "tags": ["string", "string"],
  "raw_content_reference": "string"
}