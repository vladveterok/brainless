# Phase 3: AI Processing Integration

**Status:** ToDo

## Step-by-Step Plan
1. Configure an LLM endpoint (Groq or Gemini) via an HTTP Request node in n8n.
2. Structure the prompt to extract: a title, a 3-sentence summary, 5 key takeaways, and relevant `#tags`.
3. Feed the normalized `raw_content` payload into the LLM node.
4. Process the response and use a Set Node to map the LLM's JSON into a `Standardized Insight Object`.

## Development History
*   **[2026-07-13]** Initialized Phase 3 plan.
