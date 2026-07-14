# Phase 3.5: Prompt Injection & Routing Updates

**Status:** Done

## Step-by-Step Plan
1. Add a Code Node (Parser) after the Telegram Trigger to separate URLs from custom prompts.
2. Update the Switch Node to route based on the new `$json.route` property.
3. Update extraction nodes (YouTube Transcript, Jina API) to use the clean `$json.target_url`.
4. Update Gemini AI Node to inject `$json.user_prompt` into its generation prompt.
5. Create an automated python script to safely inject these node updates into `main_workflow.json`.

## Development History
*   **[2026-07-14]** Initialized Phase 3.5 plan.
