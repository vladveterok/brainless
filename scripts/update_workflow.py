import json

with open("workflows/main_workflow.json", "r") as f:
    data = json.load(f)

# The file actually has duplicated nodes in the list. Let's fix that by taking unique IDs.
unique_nodes = {}
for n in data["nodes"]:
    if n["id"] not in unique_nodes:
        unique_nodes[n["id"]] = n

# Now modify the youtube-transcript node
youtube_node = unique_nodes.get("youtube-transcript")
if youtube_node:
    youtube_node["type"] = "n8n-nodes-base.httpRequest"
    youtube_node["typeVersion"] = 4.1
    youtube_node["parameters"] = {
        "url": "=http://youtube-extractor:5000/transcript?url={{encodeURIComponent($json.message.text)}}",
        "options": {}
    }

data["nodes"] = list(unique_nodes.values())

with open("workflows/main_workflow.json", "w") as f:
    json.dump(data, f, indent=2)

print("Updated workflow JSON safely!")
