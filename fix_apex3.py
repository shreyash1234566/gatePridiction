with open("E:/GATE PRIDICTION/gate_apex_v10.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def predict_micro(" in line:
        lines.insert(i + 1, "        return self._predict_micro_legacy(topic_preds, target_year)\n")
        break

for i, line in enumerate(lines):
    if "candidates.sort(key=lambda x: x[\"score\"], reverse=True)" in line:
        # replace the next line which is `top_40 = candidates[:40]`
        lines[i+1] = "        high_conf = [c for c in candidates if c['score'] >= 0.60]\n        top_40 = high_conf[:40]\n"
        break

with open("E:/GATE PRIDICTION/gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
