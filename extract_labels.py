import json
from collections import Counter

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract all unique micro_topic labels with counts, grouped by subject::topic
labels = Counter()
by_topic = {}
for q in data:
    s = q.get("subject", "").strip()
    t = q.get("topic", "").strip()
    m = q.get("micro_topic", "").strip()
    labels[m] += 1
    pk = f"{s}::{t}"
    if pk not in by_topic:
        by_topic[pk] = Counter()
    by_topic[pk][m] += 1

# Print grouped by topic
for pk in sorted(by_topic.keys()):
    print(f"\n=== {pk} ===")
    for label, count in by_topic[pk].most_common():
        print(f"  [{count:3d}x] {label}")

print(f"\n\nTOTAL: {len(labels)} unique micro-topic labels across {len(data)} questions")
