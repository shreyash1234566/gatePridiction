import json

with open('elite_predictions_2026.json', 'r') as f:
    data = json.load(f)

print("=" * 90)
print("🎯 GATE 2026 TOP TOPIC PREDICTIONS")
print("=" * 90)

for i, p in enumerate(data['predictions'][:25], 1):
    print(f"{i:2d}. {p['subject'][:22]:22s} | {p['topic'][:30]:30s} | {p['predicted_count']:5.2f}q | {p['confidence']:5.1f}%")

print("\n" + "=" * 90)
print("📊 SUBJECT TOTALS")
print("=" * 90)

for subj, count in data.get('subject_totals', {}).items():
    print(f"   {subj:<28s}: {count:5.1f} questions")

print(f"\n📈 Model Metrics: R² = {data['meta']['metrics'].get('R2', 'N/A')}")
