# Phase 7: Interactive Telegram Feedback (Auto-Store + Notify)

**Status:** In Progress

## Plan
1. Update `workflows/main_workflow.json` to inject the AI-generated note content (`{{$node["Set Normalized Insights"].json.content}}`) into the Telegram Send node's text parameter.
2. Ensure the resulting message cleanly formats the Markdown payload.

## Development History
- **[2026-07-15] Attempt 1:** Writing Python script `scripts/update_workflow_phase7.py` to securely update the `text` field in the Telegram Send node to append the full note content.
