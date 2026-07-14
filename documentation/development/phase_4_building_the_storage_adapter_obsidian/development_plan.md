# Phase 4: Building the Storage Adapter (Obsidian)

## Status
Done

## Step-by-Step Plan
1. Configure n8n Obsidian Storage Node.
2. Route the output from the AI Parsing node directly to the local Obsidian instance via `obsidian-local-rest-api`.
3. Format the filename and markdown payload correctly using n8n expressions.
4. Verify the note is created successfully in Obsidian.

## Development History
- **2026-07-14**:
  - Investigated issue with Obsidian storage node creating `undefined.md` with empty `{}` content.
  - Identified that the `Set Normalized Insights` node was silently failing and simply passing the raw Gemini payload through.
  - Replaced the Set node with a `Code` node for robust JSON parsing.
  - Fixed Obsidian Storage Node's body configuration: Switched `specifyBody` from `"string"` to `"raw"` and added `contentType: "raw"` and `rawContentType: "text/markdown"` root parameters. This correctly completely bypassed n8n's object coercion bugs.
  - User successfully verified perfectly formatted markdown files in Obsidian.
