# TICKET-001: Telegram Webhook Requires HTTPS

**Status:** Resolved

## Description
When attempting to execute the Telegram Trigger node on a local n8n instance, the node fails with the error: `Bad Request: bad webhook: An HTTPS URL must be provided for webhook`. This occurs because n8n is running on `http://localhost:5678` and passes this HTTP URL to the Telegram API, which strictly requires an `HTTPS` endpoint for webhooks.

## Fix History
* **[2026-07-13] Attempt 1:** Proposed updating the `docker-compose.yml` to run n8n with the `--tunnel` command. This utilizes n8n's built-in local development tunnel. 
  * **Result:** Failed. Research confirms that while the tunnel opens, the Telegram Trigger node strictly registers the webhook using the global `WEBHOOK_URL` environment variable. Since we did not set it, it defaulted to `http://localhost:5678`, causing Telegram to reject it again.
* **[2026-07-13] Attempt 2:** Expose the local n8n instance via a dedicated tunneling service (like `ngrok` or `localtunnel`), explicitly define the `WEBHOOK_URL` environment variable in `.env`, and map it into the `docker-compose.yml`. 
  * **Result:** Success. The explicit injection forces the Telegram node to use the secure HTTPS tunnel, successfully registering the webhook.
