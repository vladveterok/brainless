# Phase 2: Extraction Integration

**Status:** Done

## Step-by-Step Plan
1. Add an HTTP Request node to the **Article Route** to fetch clean Markdown via `https://r.jina.ai/{{$json.message.text}}`.
2. Add a YouTube extraction mechanism to the **YouTube Route** (pending user decision on implementation method).
3. Add **Set nodes** to normalize the output from all routes into a standard `raw_content` variable.
4. Merge all paths back together into a single pipeline using a **Merge Node** (set to "Pass-through").
5. Test all three pathways (Text, Article, YouTube).

## Development History
*   **[2026-07-13]** Initialized Phase 2 planning and requested user feedback on the YouTube extraction approach.
