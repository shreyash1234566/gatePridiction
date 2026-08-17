import json

with open("Q_unified.json", "r", encoding="utf-8") as f:
    q_data = json.load(f)

q2026 = [q for q in q_data if q["year"] == 2026]

with open("Q_2026_audit_input.json", "w", encoding="utf-8") as f:
    json.dump(q2026, f, indent=4)

print(f"Prepared 2026 target data. Count: {len(q2026)}")
