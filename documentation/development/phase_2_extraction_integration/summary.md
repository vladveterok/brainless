# Phase 2 Summary: Extraction Integration

## Overview
Phase 2 focused on successfully extracting raw text payloads from links submitted via Telegram, ensuring that the system could robustly handle both standard web articles and YouTube videos.

## Work Completed
1. **Article Extraction:** Configured the `Jina API Extract` HTTP Request node to route standard web URLs through `r.jina.ai`, returning clean markdown text.
2. **YouTube Extraction Microservice:**
   - Abandoned the fragile JS/NPM packages and the distroless n8n container constraints.
   - Designed and deployed a completely separate, dedicated Python microservice (`youtube-extractor`) within the Docker stack.
   - Utilized the robust `youtube-transcript-api` library to bypass YouTube's IP blocks and age-gate scripts.
   - Refactored `docker-compose.yml` to orchestrate both the core n8n image and the microservice cleanly.
3. **Workflow Normalization:**
   - Updated `main_workflow.json` to route YouTube URLs to an HTTP Request node targeting our internal microservice API.
   - Fixed bugs related to duplicate nodes in the original JSON structure.
   - Standardized the output payload structure across all three trigger branches (Text, Web Article, YouTube) into a normalized `raw_content` variable using Set nodes.

## Issues Resolved
- **NPM Package Fragility:** The `@endcycles/youtube-transcript` community node crashed due to missing OS dependencies (`yt-dlp` and python).
- **YouTube API XML Bug:** Bypassed the YouTube XML parsing bug (`no element found: line 1, column 0`) by forcefully busting Docker's cache and pulling the latest patched version of the Python API.
- **API Deprecation:** Handled deprecated method crashes by rewriting the API call in `app.py` to use the modern `.list_transcripts()` pattern.

## Status
Completed successfully. The n8n instance is now actively receiving and normalizing text from all three sources.
