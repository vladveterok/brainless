import json
import uuid

WORKFLOW_FILE = "workflows/main_workflow.json"

def main():
    try:
        with open(WORKFLOW_FILE, "r") as f:
            workflow = json.load(f)
            
        nodes = workflow.get("nodes", [])
        connections = workflow.get("connections", {})
        
        # 1. Create the new Code Node
        parser_node_id = str(uuid.uuid4())
        parser_js = """
const text = $json.message.text || '';
const urlRegex = /(https?:\\/\\/[^\\s]+)/;
const match = text.match(urlRegex);

let target_url = null;
let user_prompt = text.trim();
let route = 'text';

if (match) {
    target_url = match[1];
    user_prompt = text.replace(target_url, '').trim();
    
    if (target_url.includes('youtube.com') || target_url.includes('youtu.be')) {
        route = 'youtube';
    } else {
        route = 'article';
    }
}

return {
    json: {
        target_url: target_url,
        user_prompt: user_prompt,
        route: route,
        original_text: text
    }
};
"""
        
        parser_node = {
            "parameters": {
                "jsCode": parser_js
            },
            "id": parser_node_id,
            "name": "Message Parser",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [230, 300]
        }
        
        nodes.append(parser_node)
        
        # 2. Update existing nodes
        for node in nodes:
            if node["name"] == "Switch Node (Router)":
                node["position"] = [460, 300]
                # Reconfigure switch node to use route
                node["parameters"] = {
                    "mode": "rules",
                    "output": "rename",
                }
                node["parameters"]["rules"] = {
                    "values": [
                        {
                            "conditions": {
                                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                                "conditions": [{"leftValue": "={{ $json.route }}", "rightValue": "youtube", "operator": {"type": "string", "operation": "equals", "singleValue": True}}],
                                "combinator": "and"
                            },
                            "renameOutput": True,
                            "outputKey": "YouTube Route"
                        },
                        {
                            "conditions": {
                                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                                "conditions": [{"leftValue": "={{ $json.route }}", "rightValue": "article", "operator": {"type": "string", "operation": "equals", "singleValue": True}}],
                                "combinator": "and"
                            },
                            "renameOutput": True,
                            "outputKey": "Article Route"
                        },
                        {
                            "conditions": {
                                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                                "conditions": [{"leftValue": "={{ $json.route }}", "rightValue": "text", "operator": {"type": "string", "operation": "equals", "singleValue": True}}],
                                "combinator": "and"
                            },
                            "renameOutput": True,
                            "outputKey": "Text Route"
                        }
                    ]
                }
                node["parameters"]["options"] = {"fallbackOutput": False}
            
            elif node["name"] == "YouTube Transcript":
                node["parameters"]["url"] = "=http://youtube-extractor:5000/transcript?url={{encodeURIComponent($json.target_url)}}"
            
            elif node["name"] == "Jina API Extract (Article)":
                node["parameters"]["url"] = "=https://r.jina.ai/{{$json.target_url}}"
                
            elif node["name"] == "Set Text Content":
                # Text node uses original text if no url
                node["parameters"]["assignments"]["assignments"][0]["value"] = "={{$json.original_text}}"
            
            elif node["name"] == "Gemini AI Node":
                node["parameters"]["jsonBody"] = "={{ { \"contents\": [ { \"parts\": [ { \"text\": \"Custom User Instructions:\\n\" + ($node[\"Message Parser\"].json.user_prompt ? $node[\"Message Parser\"].json.user_prompt : 'None provided.') + \"\\n\\nTask:\\nReturn ONLY valid JSON with keys: 'title', 'tags', and 'content'.\\nIf no Custom User Instructions are provided, 'content' must be a 3-sentence summary and 5 key takeaways formatted in Markdown.\\nIf Custom User Instructions ARE provided, ignore the default summary format. Instead, 'content' must contain the detailed response to the Custom User Instructions formatted in Markdown.\\n\\nText: \" + ($json.raw_content || $json.text || $json.data || $json.original_text || '') } ] } ], \"generationConfig\": { \"responseMimeType\": \"application/json\" } } }}"
                node["retryOnFail"] = True
                node["maxTries"] = 5
                node["waitBetweenTries"] = 15000

        # 3. Update connections
        # Telegram Trigger -> Message Parser
        connections["Telegram Trigger"] = {
            "main": [
                [
                    {
                        "node": "Message Parser",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
        
        # Message Parser -> Switch Node
        connections["Message Parser"] = {
            "main": [
                [
                    {
                        "node": "Switch Node (Router)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
        
        with open(WORKFLOW_FILE, "w") as f:
            json.dump(workflow, f, indent=2)
            
        print("Workflow successfully updated for Phase 3.5.")

    except Exception as e:
        print(f"Error updating workflow: {e}")

if __name__ == "__main__":
    main()
