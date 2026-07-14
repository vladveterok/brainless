# Phase 3.5 Summary: Prompt Parsing & Dynamic Injection

## Goal
To introduce the ability to send both a URL and a custom instruction (prompt) to the AI Node within a single Telegram message.

## Implementation Details

1. **Ingestion Layer Modifications**
   - Introduced a `Message Parser` Code Node immediately following the Telegram trigger.
   - The parser uses Regex to extract any valid URL from the incoming text.
   - The remaining text is trimmed and stored as `user_prompt`.
   - Determines the `route` (youtube, article, text) based on the URL domain.

2. **Routing Adjustments**
   - Reconfigured the `Switch Node` to route traffic strictly based on the extracted `route` variable, decoupling the routing logic from the raw message text.
   - Downstream extractor nodes (`YouTube Transcript`, `Jina API`) were updated to explicitly fetch content from the `target_url` variable.

3. **AI Schema Refactoring**
   - The Gemini AI Node was updated to conditionally accept the `user_prompt` from the Message Parser.
   - Refactored the output schema to ensure predictability for downstream storage (Phase 4).
   - The AI Node now strictly outputs:
     - `title`
     - `tags`
     - `content`
   - If a custom prompt is provided, the `content` field is populated with a free-form markdown response fulfilling the instruction. If no prompt is provided, it defaults to a standard 3-sentence summary and 5 key takeaways.

4. **Resiliency**
   - Configured automated retries (5 tries, 15-second delay) on the Gemini AI Node to handle temporary 503 HTTP spikes from the Google API.

## Status
Completed and verified. The workflow is capable of dynamically adjusting its output based on user instructions while maintaining a strict JSON schema for downstream data persistence.
