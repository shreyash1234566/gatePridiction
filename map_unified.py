import json

with open("Q.json", "r", encoding="utf-8") as f:
    q_data = json.load(f)

with open("golden_taxonomy.json", "r", encoding="utf-8") as f:
    golden = json.load(f)

# Re-map Q.json to use the new taxonomy
# In the old structure, q["topic"] was the mid-level and q["micro_topic"] was the raw leaf.
# Now:
#   q["subject"] remains
#   q["concept"] = <discovered from golden taxonomy>
#   q["micro_topic"] = <original generic name, unless standardized during audit>
# Because we are doing a structural change, we will update "topic" to be the new "concept"
# to keep code breakages minimal, or create a 'concept' key. We will keep 'topic' as the concept key.

# Build a reverse lookup from micro_topic -> concept
reverse_lookup = {}
for subj, concepts in golden.items():
    if subj not in reverse_lookup:
        reverse_lookup[subj] = {}
    for concept, data in concepts.items():
        for mt in data["micro_topics"]:
            reverse_lookup[subj][mt] = concept

c = 0
for q in q_data:
    subj = q["subject"]
    mt = q.get("micro_topic", "")

    # Try looking it up
    target_concept = reverse_lookup.get(subj, {}).get(mt)
    if target_concept:
        q["topic"] = target_concept
        c += 1
    else:
        # It's an unmapped one (like the 2026 ones if they aren't in canonical yet)
        pass

with open("Q_unified.json", "w", encoding="utf-8") as f:
    json.dump(q_data, f, indent=4)
print(f"Mapped {c} questions to Golden Concepts.")
