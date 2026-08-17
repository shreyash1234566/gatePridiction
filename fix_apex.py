import re
with open("E:/GATE PRIDICTION/gate_apex_v10.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "if True: \# user requested raw microtopics\n" in line:
        continue
    if "if True:\n            return self._predict_micro_legacy(topic_preds, target_year)" in line:
        continue
    new_lines.append(line)

code = "".join(new_lines)
code = code.replace("if True:\n            return self._predict_micro_legacy(topic_preds, target_year)", "")
code = code.replace(r"if True:\n            return self._predict_micro_legacy(topic_preds, target_year)", "")

# Find predict_micro and make it ALWAYS call legacy
pattern = r"def predict_micro\(self, topic_preds: List\[dict\], target_year: int\) -> List\[dict\]:\n\s+print\(f\"\n🔬 Micro‑topic predictions for \{target_year\} \(Canonical Dirichlet\) …\"\)\n\s+parent_quota = \{f\"\{p\['subject'\]\}::\{p\['topic'\]\}\": p\[\"predicted_count\"\] for p in topic_preds\}\n\n\s+if not self\.canonical_taxonomy:\n\s+return self\._predict_micro_legacy\(topic_preds, target_year\)"

replacement = """def predict_micro(self, topic_preds: List[dict], target_year: int) -> List[dict]:
        # User requested explicitly to predict raw microtopics, not concepts
        return self._predict_micro_legacy(topic_preds, target_year)
        
        # Dead code below to avoid removing everything:
        print(f"\n🔬 Micro‑topic predictions for {target_year} (Canonical Dirichlet) …")
        parent_quota = {f"{p['subject']}::{p['topic']}": p["predicted_count"] for p in topic_preds}

        if not self.canonical_taxonomy:
            return self._predict_micro_legacy(topic_preds, target_year)"""

code = re.sub(pattern, replacement, code)

# Fix predict_micro_new dynamic threshold (>= 0.60)
pattern_new = r"candidates\.sort\(key=lambda x: x\[\"score\"\], reverse=True\)\n\s+top_40 = candidates\[:40\]"
replacement_new = """candidates.sort(key=lambda x: x["score"], reverse=True)
        # Apply high confidence filter: score >= 0.60
        high_conf = [c for c in candidates if c["score"] >= 0.60]
        # But allow at least some if they are really high, max 40
        top_40 = high_conf[:40]"""

code = re.sub(pattern_new, replacement_new, code)

with open("E:/GATE PRIDICTION/gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Fixed gate_apex_v10.py")
