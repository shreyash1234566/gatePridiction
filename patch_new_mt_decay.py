import re
import json
from collections import defaultdict
from pathlib import Path

with open("gate_apex_v10.py", "r", encoding="utf-8") as f:
    text = f.read()

# Make the pattern strict and literal around the entire old predict_micro_new logic
# finding from its signature up to its return
pattern = re.compile(r"    def predict_micro_new\(self, target_year: int\) -> List\[dict\]:.*?return top_40\n", re.DOTALL)
match = pattern.search(text)

if not match:
    # Maybe top_40 wasn't matched properly or the signature changed.
    # Let's verify by just printing success or fail.
    print("Failed to find predict_micro_new method body.")
    exit(1)

new_method = """    def predict_micro_new(self, target_year: int, max_new: int = 20) -> List[dict]:
        '''Predict unseen "New MT" micro-topics using a 3-signal architecture with syllabus exhaustion + decay.'''
        print(f"\n✨ Predicting New MT candidates for {target_year} …")

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
                seen_labels_normalized.add(f"{parts[0]}::{parts[1]}::{norm_topic(parts[2]).lower()}")

        # PRE-COMPUTE Syllabus exhaustion per topic
        # Exhaustion Penalty = unseen / total_syllabus
        topic_exhaustion = {}
        for subj, topics in syllabus.items():
            for topic, mt_list in topics.items():
                pk = f"{subj}::{topic}"
                total_syl = len(mt_list)
                unseen = 0
                for mt in mt_list:
                    if f"{subj}::{topic}::{norm_topic(mt).lower()}" not in seen_labels_normalized:
                        unseen += 1
                val = (unseen / total_syl) if total_syl > 0 else 0.0
                topic_exhaustion[pk] = val

        candidates = []
        for subj, topics in syllabus.items():
            for topic, mt_list in topics.items():
                pk = f"{subj}::{topic}"
                exhaust = topic_exhaustion.get(pk, 0.0)
                
                for mt in mt_list:
                    norm_mt = norm_topic(mt).lower()
                    if f"{subj}::{topic}::{norm_mt}" not in seen_labels_normalized:
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

                        base_score = (0.45 * s1 + 0.30 * s2 + 0.25 * s3) * exhaust

                        candidates.append({
                            "subject": subj,
                            "topic": topic,
                            "micro_topic": mt,
                            "canonical_concept": mt,
                            "raw_labels": f"{mt} [NEW]",
                            "predicted_count": 0.5,
                            "confidence": round((0.4 + base_score * 0.4) * 100, 1),
                            "trend": "New MT",
                            "base_score": base_score,
                            "score": base_score,
                            "tier": "Discovery",
                            "alpha": 0.0,
                            "theta": 0.0
                        })

        final_selected = []
        topic_picks = defaultdict(int)

        while len(final_selected) < max_new and candidates:
            # Re-decay
            for c in candidates:
                pk = f"{c['subject']}::{c['topic']}"
                c["score"] = c["base_score"] * (0.3 ** topic_picks[pk])
            
            candidates.sort(key=lambda x: x["score"], reverse=True)
            best = candidates.pop(0)

            if best["score"] >= 0.10:
                final_selected.append(best)
                topic_picks[f"{best['subject']}::{best['topic']}"] += 1
            else:
                break
                
        print(f"   ✓ Generated candidates, selected Top {len(final_selected)} New MTs (Decay applied)")
        return final_selected
"""

new_text = pattern.sub(new_method, text)

with open("gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(new_text)

print("SUCCESS: predict_micro_new replaced")
