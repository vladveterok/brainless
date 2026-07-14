---
title: "TICKET-002: Gemini API Rate Limit / Model Issue"
status: "Resolved"
---

# Description
The n8n workflow was failing with a `429 Too Many Requests` error, explicitly stating a quota of 20 requests was exceeded for `gemini-3.5-flash`.
After investigation using a direct `curl` command to the API, it was discovered that `gemini-3.5-flash` (which `gemini-flash-latest` resolves to) has a strict Free Tier quota of **20 requests per day**. This tiny daily quota was exhausted during standard debugging.

# Fix History
*   **Attempt 1:** Theorized Telegram webhooks were looping. (Failed - Disproven by logs showing only 1 execution).
*   **Attempt 2:** Theorized n8n was looping due to retry configurations. (Failed - Retries only multiply to 5, not enough to hit standard minute-bucket quotas).
*   **Attempt 3:** Direct API test bypassing n8n. (Success - Revealed the quota was a strict 20/day limit for `gemini-3.5-flash`).
*   **Attempt 4:** Changed model to `gemini-2.5-flash-lite`. (Failed - API returned 404 Not Found, stating the model is no longer available to new users).
*   **Attempt 5:** Changed model to `gemini-1.5-flash`. (Failed - API returned 404 Not Found, model is completely unsupported for API v1beta in 2026).
*   **Attempt 6:** Ran a direct curl test against remaining candidate models. `gemini-2.0-flash` and `gemini-2.0-flash-lite` returned 429 Quota Exceeded (capped at 20/day). `gemini-flash-lite-latest` returned a successful 200 OK.
*   **Final Solution:** Changed the target model in the `Gemini AI Node` to `gemini-flash-lite-latest`, which guarantees a generous Free Tier quota without returning a deprecation error.
