import json

with open("workflows/main_workflow.json", "r") as f:
    data = json.load(f)

for node in data["nodes"]:
    if node["name"] == "Telegram Send":
        node["parameters"]["text"] = "✅ Successfully saved to Vault!\n\n📄 **{{$node[\"Set Normalized Insights\"].json.title}}**\n🏷️ Tags: {{$node[\"Set Normalized Insights\"].json.tags.join(', ')}}\n\n---\n{{$node[\"Set Normalized Insights\"].json.content}}"

with open("workflows/main_workflow.json", "w") as f:
    json.dump(data, f, indent=2)

print("Successfully updated main_workflow.json")
