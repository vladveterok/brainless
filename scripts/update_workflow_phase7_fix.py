import json

file_path = "/Users/altruisticant/Projects/brainless/workflows/main_workflow.json"

with open(file_path, "r") as f:
    data = json.load(f)

for node in data["nodes"]:
    if node["name"] == "Set Normalized Insights":
        node["parameters"]["jsCode"] = """const responseText = $json.candidates[0].content.parts[0].text;

// Strip potential markdown backticks just in case
const cleanJson = responseText.replace(/```json\\n?|```/g, '').trim();
const parsed = JSON.parse(cleanJson);

const tags = parsed.tags || [];
const markdownContent = `---\\ntags: [${tags.join(', ')}]\\nsource: ${$node["Message Parser"].json.route}\\n---\\n# ${parsed.title}\\n\\n${parsed.content}`;

const telegramSafeContent = (parsed.content || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

const telegramSafeTitle = (parsed.title || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

return {
    json: {
        title: parsed.title,
        tags: tags,
        content: parsed.content,
        telegram_content: telegramSafeContent,
        telegram_title: telegramSafeTitle,
        base64_content: Buffer.from(markdownContent).toString('base64')
    }
};"""
    if node["name"] == "Telegram Send":
        node["parameters"]["text"] = "=\u2705 <b>Successfully saved to Vault!</b>\n\n\ud83d\udcc4 <b>{{$node[\"Set Normalized Insights\"].json.telegram_title}}</b>\n\ud83c\udff7\ufe0f Tags: {{$node[\"Set Normalized Insights\"].json.tags.join(', ')}}\n\n---\n{{$node[\"Set Normalized Insights\"].json.telegram_content}}"
        node["parameters"]["additionalFields"] = {
            "parse_mode": "HTML"
        }

with open(file_path, "w") as f:
    json.dump(data, f, indent=2)

print("Successfully applied HTML bypass fix")
