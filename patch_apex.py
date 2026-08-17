import re

with open('gate_apex_v10.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add predict_micro_new method right after _predict_micro_legacy ends

predict_micro_new_code = """
    def predict_micro_new(self, target_year: int) -> List[dict]:
        '''Predict unseen "New MT" micro-topics using a 3-signal architecture.'''
        print(f"\\n✨ Predicting New MT candidates for {target_year} …")

        syllabus_path = Path("gate_syllabus.json")
        if not syllabus_path.exists():
            print("   ⚠️  gate_syllabus.json not found. Cannot predict new MTs.")
            return []

        with open(syllabus_path, "r", encoding="utf-8") as f:
            syllabus = json.load(f)

        # Determine first appearance year of each micro topic (< target_year)
        first_seen = {}
        for mk, d in self.micro_data.items():
            valid_years = [y for y, c in zip(d["years"], d["counts"]) if y < target_year and c > 0]
            if valid_years:
                first_seen[mk] = min(valid_years)

        topic_new_mt_count = defaultdict(int)
        subj_new_mt_count = defaultdict(int)
        topic_appearances = defaultdict(set)
        topic_last_seen = {}

        for k, d in self.topic_data.items():
            pk = f"{d['subject']}::{d['topic']}"
            valid_years = [y for y, c in zip(d["years"], d["counts"]) if y < target_year and c > 0]
            if valid_years:
                for y in valid_years:
                    topic_appearances[pk].add(y)
                topic_last_seen[pk] = max(valid_years)

        for mk, yr in first_seen.items():
            if yr >= 2011:
                parts = mk.split("::")
                subj, topic = parts[0], parts[1]
                pk = f"{subj}::{topic}"
                topic_new_mt_count[pk] += 1
                subj_new_mt_count[subj] += 1

        subj_total_qs = defaultdict(float)
        for mk, d in self.micro_data.items():
            parts = mk.split("::")
            subj = parts[0]
            count = sum(c for y, c in zip(d["years"], d["counts"]) if y >= 2011 and y < target_year)
            subj_total_qs[subj] += count

        topic_rate = {}
        for pk in topic_appearances:
            apps = len(topic_appearances[pk])
            topic_rate[pk] = topic_new_mt_count[pk] / apps if apps > 0 else 0

        subj_rate = {}
        for s in SECTION_DISTRIBUTION:
            if subj_total_qs[s] > 0:
                subj_rate[s] = subj_new_mt_count[s] / subj_total_qs[s]
            else:
                subj_rate[s] = 0

        max_t_rate = max(topic_rate.values()) if topic_rate else 1.0
        if max_t_rate == 0: max_t_rate = 1.0
        for pk in topic_rate:
            topic_rate[pk] /= max_t_rate

        seen_labels_normalized = set()
        for mk in first_seen.keys():
            parts = mk.split("::")
            if len(parts) >= 3:
                seen_labels_normalized.add(norm_topic(parts[2]).lower())

        candidates = []
        for subj, topics in syllabus.items():
            for topic, mt_list in topics.items():
                pk = f"{subj}::{topic}"
                for mt in mt_list:
                    norm_mt = norm_topic(mt).lower()
                    if norm_mt not in seen_labels_normalized:
                        s1 = topic_rate.get(pk, 0.0)
                        s2 = subj_rate.get(subj, 0.0)

                        last_yr = topic_last_seen.get(pk, -1)
                        if last_yr > 0:
                            gap = target_year - last_yr
                            if gap == 1:
                                s3 = 1.0
                            elif gap in [2, 3]:
                                s3 = 0.5
                            else:
                                s3 = 0.3
                        else:
                            s3 = 0.1

                        # Composite Score
                        score = 0.45 * s1 + 0.30 * s2 + 0.25 * s3

                        candidates.append({
                            "subject": subj,
                            "topic": topic,
                            "micro_topic": mt,
                            "canonical_concept": mt,
                            "raw_labels": f"{mt} [NEW]",
                            "predicted_count": 0.5,
                            "confidence": round((0.4 + score * 0.4) * 100, 1),
                            "trend": "New MT Candidate",
                            "score": score,
                            "tier": "Discovery",
                            "alpha": 0.0,
                            "theta": 0.0
                        })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        top_40 = candidates[:40]
        print(f"   ✓ Generated candidates, selected Top {len(top_40)} New MTs")
        return top_40
"""

# Find insertion point for predict_micro_new
injection_pattern = r'(\s+print\(f"   ✓ \{len\(result\)\} micro‑topic predictions \(legacy EMA mode\)"\)\n\s+return result\n)'
match = re.search(injection_pattern, code)
if not match:
    # also try searching for just normal print and return
    injection_pattern = r'(\s+return result\n)(\n# --+\n# 10\.  Validator)'
    code = re.sub(injection_pattern, r'\1' + predict_micro_new_code + r'\2', code)
else:
    code = code[:match.end()] + "\n" + predict_micro_new_code + code[match.end():]

# 2. Modify Validator to use predict_micro combined with predict_micro_new
val_pattern = r'(pred_micro = defaultdict\(float\)\n\s+pred_canon = defaultdict\(float\)\n)'

patch_str = """
            # Build micro-topic predictions: EXPAND concepts back to raw labels
"""
old_validator_block = """
            # Build micro-topic predictions: EXPAND concepts back to raw labels
            # This fixes the M_Hit measurement bug: the model predicts concepts
            # ("Minimum Spanning Trees") but M_Hit compares raw labels ("Kruskal's Algorithm").
            # We reverse-map each concept → all known raw labels for that concept,
            # distributing predicted_count by historical frequency within the concept.
            pred_micro = defaultdict(float)
            pred_canon = defaultdict(float)
"""
new_validator_block = """
            # Combine Old (250) + New (40) MTs
            # First, fetch New MT predictions
            buf3 = io.StringIO()
            sys.stdout = buf3
            try:
                micro_preds_new = self.pred.predict_micro_new(ty)
            finally:
                sys.stdout = sys.__stdout__

            micro_preds = micro_preds[:250] + micro_preds_new

            # Build micro-topic predictions: EXPAND concepts back to raw labels
            # This fixes the M_Hit measurement bug: the model predicts concepts
            # ("Minimum Spanning Trees") but M_Hit compares raw labels ("Kruskal's Algorithm").
            # We reverse-map each concept → all known raw labels for that concept,
            # distributing predicted_count by historical frequency within the concept.
            pred_micro = defaultdict(float)
            pred_canon = defaultdict(float)
"""
code = code.replace(old_validator_block, new_validator_block)

# 3. Modify main() to call predict_micro_new and combine predictions
main_micro_pattern = """
    predictions = final.predict_topics(2027)
    micro_predictions = final.predict_micro(predictions, 2027)
"""
main_micro_new = """
    predictions = final.predict_topics(2027)
    micro_predictions_old = final.predict_micro(predictions, 2027)
    micro_predictions_new = final.predict_micro_new(2027)

    micro_predictions = micro_predictions_old[:250] + micro_predictions_new
"""
code = code.replace(main_micro_pattern, main_micro_new)


with open('gate_apex_v10.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched gate_apex_v10.py")
