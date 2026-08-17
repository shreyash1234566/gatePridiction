import json

with open("Q_2026_audit_input.json", "r", encoding="utf-8") as f:
    q2026 = json.load(f)

with open("golden_taxonomy.json", "r", encoding="utf-8") as f:
    golden = json.load(f)

# Prepare compact question records (trim long text to save tokens)
compact_q = []
for i, q in enumerate(q2026):
    compact_q.append({
        "idx": i,
        "subject": q["subject"],
        "topic": q.get("topic", ""),
        "micro_topic": q.get("micro_topic", ""),
        "question_text": (q.get("question_text", "") or "")[:500],
        "choices": q.get("choices", {}),
        "question_number": q.get("question_number", i)
    })

args_payload = {
    "questions": compact_q,
    "golden": golden
}

with open("audit_args.json", "w", encoding="utf-8") as f:
    json.dump(args_payload, f, indent=2)

print(f"Prepared {len(compact_q)} questions with golden taxonomy for workflow args.")
