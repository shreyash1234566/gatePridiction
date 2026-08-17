import json

with open("canonical_taxonomy.json", "r", encoding="utf-8") as f:
    tax = json.load(f)

golden = {}
for key, entry in tax.items():
    subj = entry["subject"]
    if subj not in golden:
        golden[subj] = {}

    for concept in entry.get("canonical_concepts", []):
        if concept not in golden[subj]:
            golden[subj][concept] = {"micro_topics": []}

    if "label_to_concept" in entry:
        for raw_label, concept in entry["label_to_concept"].items():
            if raw_label not in golden[subj][concept]["micro_topics"]:
                golden[subj][concept]["micro_topics"].append(raw_label)

with open("golden_taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(golden, f, indent=4)
print("Golden taxonomy created with 2-tier (Concept -> Micro-topic) inside Subject.")
