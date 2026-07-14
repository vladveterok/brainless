import json

with open('workflows/main_workflow.json', 'r') as f:
    wf = json.load(f)

# The new nodes
gemini_node = {
  "parameters": {
    "method": "POST",
    "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={{$env[\"GEMINI_API_KEY\"]}}",
    "sendBody": True,
    "specifyBody": "json",
    "jsonBody": "={ \"contents\": [ { \"parts\": [ { \"text\": \"Extract a title, a 3-sentence summary, 5 key takeaways, and relevant tags (starting with #) from the following text. Return ONLY valid JSON with keys: 'title', 'summary', 'key_takeaways', 'tags'.\\n\\nText: \" + JSON.stringify($json.raw_content) } ] } ], \"generationConfig\": { \"responseMimeType\": \"application/json\" } }",
    "options": {}
  },
  "id": "gemini-ai-node",
  "name": "Gemini AI Node",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [
    1500,
    300
  ]
}

set_insights_node = {
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "id": "title",
          "name": "title",
          "value": "={{ JSON.parse($json.candidates[0].content.parts[0].text).title }}",
          "type": "string"
        },
        {
          "id": "summary",
          "name": "summary",
          "value": "={{ JSON.parse($json.candidates[0].content.parts[0].text).summary }}",
          "type": "string"
        },
        {
          "id": "key_takeaways",
          "name": "key_takeaways",
          "value": "={{ JSON.parse($json.candidates[0].content.parts[0].text).key_takeaways }}",
          "type": "array"
        },
        {
          "id": "tags",
          "name": "tags",
          "value": "={{ JSON.parse($json.candidates[0].content.parts[0].text).tags }}",
          "type": "array"
        }
      ]
    },
    "options": {}
  },
  "id": "set-normalized-insights",
  "name": "Set Normalized Insights",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3.2,
  "position": [
    1800,
    300
  ]
}

# Remove if exists (idempotency)
wf['nodes'] = [n for n in wf['nodes'] if n['id'] not in ["gemini-ai-node", "set-normalized-insights"]]

# Find Merge Payload node (if there are duplicates somehow, we just append to nodes)
wf['nodes'].append(gemini_node)
wf['nodes'].append(set_insights_node)

# Connections update
if "Merge Payload" in wf['connections']:
    wf['connections']["Merge Payload"] = {
        "main": [
            [
                {
                    "node": "Gemini AI Node",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }
else:
    wf['connections']["Merge Payload"] = { "main": [ [ { "node": "Gemini AI Node", "type": "main", "index": 0 } ] ] }

wf['connections']["Gemini AI Node"] = {
    "main": [
        [
            {
                "node": "Set Normalized Insights",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

with open('workflows/main_workflow.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Updated workflow JSON successfully.")
