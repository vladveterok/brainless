import json
import os

def update_workflow():
    workflow_path = "workflows/main_workflow.json"
    
    with open(workflow_path, "r") as f:
        workflow = json.load(f)
        
    # Check if Obsidian Storage Node already exists
    node_exists = False
    for node in workflow.get("nodes", []):
        if node.get("name") == "Obsidian Storage Node":
            node_exists = True
            break
            
    if not node_exists:
        obsidian_node = {
            "parameters": {
                "method": "POST",
                "url": "=https://host.docker.internal:27124/vault/{{encodeURIComponent($json.title)}}.md",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "value": "=Bearer {{$env[\"OBSIDIAN_API_KEY\"]}}"
                        }
                    ]
                },
                "sendBody": True,
                "contentType": "raw",
                "rawContentType": "text/markdown",
                "body": "=---\ntags: [{{$json.tags.join(', ')}}]\nsource: {{$node[\"Message Parser\"].json.route}}\n---\n# {{$json.title}}\n\n{{$json.content}}",
                "options": {
                    "allowUnauthorizedCerts": True
                }
            },
            "id": "obsidian-storage-node",
            "name": "Obsidian Storage Node",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [
                2100,
                300
            ]
        }
        workflow["nodes"].append(obsidian_node)
        print("Added Obsidian Storage Node")
        
    # Add connection
    if "Set Normalized Insights" not in workflow["connections"]:
        workflow["connections"]["Set Normalized Insights"] = {
            "main": [
                [
                    {
                        "node": "Obsidian Storage Node",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
        print("Connected Set Normalized Insights to Obsidian Storage Node")
        
    with open(workflow_path, "w") as f:
        json.dump(workflow, f, indent=2)

if __name__ == "__main__":
    update_workflow()
