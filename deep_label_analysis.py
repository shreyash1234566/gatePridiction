"""
Deep analysis: For each subject::topic, show question text + micro_topic
so we can see where the SAME type of question got different labels.
"""
import json
from collections import defaultdict

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Group by subject::topic::micro_topic, show question text snippets
by_topic = defaultdict(lambda: defaultdict(list))
for q in data:
    s = q.get("subject", "").strip()
    t = q.get("topic", "").strip()
    m = q.get("micro_topic", "").strip()
    txt = q.get("question_text", "")[:120].replace("\n", " ")
    yr = q.get("year", "?")
    by_topic[f"{s}::{t}"][m].append(f"[{yr}] {txt}")

for pk in sorted(by_topic.keys()):
    labels = by_topic[pk]
    print(f"\n{'='*80}")
    print(f"  {pk}")
    print(f"  {len(labels)} micro-topics, {sum(len(v) for v in labels.values())} questions")
    print(f"{'='*80}")
    for m in sorted(labels.keys()):
        qs = labels[m]
        print(f"\n  [{len(qs):2d}x] {m}")
        for q in qs[:3]:  # Show first 3 questions
            print(f"        {q}")
        if len(qs) > 3:
            print(f"        ... +{len(qs)-3} more")
