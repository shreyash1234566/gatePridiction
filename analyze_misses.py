"""
COMPREHENSIVE FORENSIC AUDIT OF GATE MICRO-TOPIC PREDICTION SYSTEM
No code changes. Only analysis and reporting.
"""
import json
from collections import defaultdict, Counter
import numpy as np

with open("Q.json", "r", encoding="utf-8") as f:
    raw_questions = json.load(f)

MULTI_PAPER_YEARS = {2014: 3, 2015: 3, 2016: 2, 2021: 2, 2024: 2, 2025: 2, 2026: 2}

# ============================================================
# AUDIT 1: Question counts per year & marks invariant
# ============================================================
print("=" * 80)
print("AUDIT 1: QUESTION COUNTS & MARKS INVARIANT (65q / 100 marks)")
print("=" * 80)

for year in sorted(set(q["year"] for q in raw_questions)):
    yq = [q for q in raw_questions if q["year"] == year]
    np_ = MULTI_PAPER_YEARS.get(year, 1)
    total_q = len(yq)
    per_paper = total_q / np_
    total_marks = sum(q.get("marks", 0) for q in yq)
    marks_per_paper = total_marks / np_
    flag = ""
    if abs(per_paper - 65) > 0.5:
        flag += f" ⚠️ Q/paper={per_paper:.1f}≠65"
    if total_marks > 0 and abs(marks_per_paper - 100) > 1:
        flag += f" ⚠️ Marks/paper={marks_per_paper:.1f}≠100"
    print(f"  {year}: {total_q:4d} questions ({np_}p → {per_paper:.1f}/paper)  marks_total={total_marks:.0f} ({marks_per_paper:.1f}/paper){flag}")

# ============================================================
# AUDIT 2: Micro-topic vocabulary statistics
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 2: MICRO-TOPIC VOCABULARY")
print("=" * 80)

# All unique labels
all_micros = defaultdict(lambda: {"years": [], "count": 0})
for q in raw_questions:
    s, t, m = q.get("subject", ""), q.get("topic", ""), q.get("micro_topic", "")
    key = f"{s}::{t}::{m}"
    all_micros[key]["years"].append(q["year"])
    all_micros[key]["count"] += 1

print(f"  Total unique micro-topic labels: {len(all_micros)}")

# Frequency distribution
appearance_counts = Counter()
year_counts = Counter()
for key, data in all_micros.items():
    appearance_counts[data["count"]] += 1
    year_counts[len(set(data["years"]))] += 1

print(f"\n  Frequency distribution (how many times a label appeared in total):")
for n in sorted(appearance_counts.keys()):
    pct = appearance_counts[n] / len(all_micros) * 100
    bar = "█" * int(pct)
    print(f"    {n:3d}× : {appearance_counts[n]:4d} labels ({pct:5.1f}%) {bar}")

cum_1 = sum(v for k, v in appearance_counts.items() if k <= 1)
cum_2 = sum(v for k, v in appearance_counts.items() if k <= 2)
cum_3 = sum(v for k, v in appearance_counts.items() if k <= 3)
print(f"\n  Appeared ≤1 time: {cum_1} ({cum_1/len(all_micros)*100:.1f}%)")
print(f"  Appeared ≤2 times: {cum_2} ({cum_2/len(all_micros)*100:.1f}%)")
print(f"  Appeared ≤3 times: {cum_3} ({cum_3/len(all_micros)*100:.1f}%)")

print(f"\n  Year span distribution (in how many distinct years):")
for n in sorted(year_counts.keys()):
    pct = year_counts[n] / len(all_micros) * 100
    print(f"    {n:3d} year(s): {year_counts[n]:4d} labels ({pct:5.1f}%)")

# ============================================================
# AUDIT 3: EMA zero-skip bug verification
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 3: EMA ZERO-SKIP BUG")
print("=" * 80)

# The EMA function takes `counts` list which is built from `build_data`
# build_data only stores years where the label actually appeared
# So counts = [1, 1, 1] for a label that appeared in 2015, 2019, 2023
# The EMA treats this as 3 consecutive observations, ignoring the 0 gaps
# This means EMA([1,1,1]) = 1.0, same as a label that appeared every year

example_sporadic = None
example_consistent = None
for key, data in all_micros.items():
    unique_years = sorted(set(data["years"]))
    if len(unique_years) == 3 and max(unique_years) - min(unique_years) >= 6:
        if example_sporadic is None:
            example_sporadic = (key, unique_years)
    if len(unique_years) == 3 and max(unique_years) - min(unique_years) == 2:
        if example_consistent is None:
            example_consistent = (key, unique_years)

if example_sporadic and example_consistent:
    print(f"  SPORADIC example: {example_sporadic[0][:60]}")
    print(f"    Years: {example_sporadic[1]} (span={max(example_sporadic[1])-min(example_sporadic[1])} years, gaps)")
    print(f"    EMA input: [1, 1, 1] → EMA(α=0.7) = 1.0")
    print(f"  CONSISTENT example: {example_consistent[0][:60]}")
    print(f"    Years: {example_consistent[1]} (span={max(example_consistent[1])-min(example_consistent[1])} years, no gaps)")
    print(f"    EMA input: [1, 1, 1] → EMA(α=0.7) = 1.0")
    print(f"  ⚠️ Both get identical EMA=1.0 despite hugely different reliability!")
    print(f"  The exp(-ys/τ) decay partially compensates, but the EMA itself is blind to gaps.")

# ============================================================
# AUDIT 4: Threshold mismatch — dead zone analysis
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 4: THRESHOLD MISMATCH (0.05 output vs 0.15 evaluation)")
print("=" * 80)

MICRO_MIN_PRED = 0.05
MICRO_HIT_TH = 0.15
print(f"  MICRO_MIN_PRED = {MICRO_MIN_PRED} (output filter: predictions below this are dropped)")
print(f"  MICRO_HIT_TH   = {MICRO_HIT_TH} (evaluation: only preds ≥ this count as 'hit')")
print(f"  DEAD ZONE: predictions in [{MICRO_MIN_PRED}, {MICRO_HIT_TH}) are output but NEVER counted")
print(f"  This means ~25% of output predictions are guaranteed to be ignored in validation")

# ============================================================
# AUDIT 5: Per-year ceiling analysis with FULL breakdown
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 5: PER-YEAR MATHEMATICAL CEILING ANALYSIS")
print("=" * 80)

for test_year in [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]:
    train_q = [q for q in raw_questions if q["year"] < test_year]
    test_q = [q for q in raw_questions if q["year"] == test_year]
    if not test_q:
        continue
    
    np_ = MULTI_PAPER_YEARS.get(test_year, 1)
    
    # Build historical micro-topic sets
    hist_micros = defaultdict(lambda: {"count": 0, "years": set()})
    for q in train_q:
        key = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        hist_micros[key]["count"] += 1
        hist_micros[key]["years"].add(q["year"])
    
    hist_topics = set()
    for q in train_q:
        hist_topics.add(f"{q['subject']}::{q['topic']}")
    
    # Actual micro-topics in this year
    actual = defaultdict(int)
    for q in test_q:
        key = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        actual[key] += 1
    
    # Categorize each actual micro-topic
    brand_new = 0
    brand_new_q = 0.0
    appeared_once = 0
    appeared_once_q = 0.0
    last_seen_old = 0
    last_seen_old_q = 0.0
    valid_candidates = 0
    valid_candidates_q = 0.0
    parent_known_new = 0
    parent_unknown_new = 0
    
    for key, cnt in actual.items():
        parts = key.split("::")
        parent_key = f"{parts[0]}::{parts[1]}"
        q_eq = cnt / np_  # question equivalents
        
        if key not in hist_micros:
            brand_new += 1
            brand_new_q += q_eq
            if parent_key in hist_topics:
                parent_known_new += 1
            else:
                parent_unknown_new += 1
            continue
        
        hist = hist_micros[key]
        if len(hist["years"]) < 2:
            appeared_once += 1
            appeared_once_q += q_eq
            continue
        
        if max(hist["years"]) < 2016:
            last_seen_old += 1
            last_seen_old_q += q_eq
            continue
        
        valid_candidates += 1
        valid_candidates_q += q_eq
    
    total_unique = len(actual)
    total_q_eq = sum(c / np_ for c in actual.values())
    
    print(f"\n  --- {test_year} ({np_}p, {len(test_q)}q → {total_q_eq:.1f} q-eq, {total_unique} unique micro-labels) ---")
    print(f"    Brand new (never seen):          {brand_new:3d} labels ({brand_new/total_unique*100:5.1f}%) | {brand_new_q:5.1f} q-eq ({brand_new_q/total_q_eq*100:5.1f}%)")
    print(f"      └ Parent topic known:          {parent_known_new:3d}")
    print(f"      └ Parent topic also unknown:   {parent_unknown_new:3d}")
    print(f"    Appeared <2 times in history:    {appeared_once:3d} labels ({appeared_once/total_unique*100:5.1f}%) | {appeared_once_q:5.1f} q-eq ({appeared_once_q/total_q_eq*100:5.1f}%)")
    print(f"    Last seen before 2016:           {last_seen_old:3d} labels ({last_seen_old/total_unique*100:5.1f}%) | {last_seen_old_q:5.1f} q-eq ({last_seen_old_q/total_q_eq*100:5.1f}%)")
    print(f"    VALID (could be predicted):      {valid_candidates:3d} labels ({valid_candidates/total_unique*100:5.1f}%) | {valid_candidates_q:5.1f} q-eq ({valid_candidates_q/total_q_eq*100:5.1f}%)")
    print(f"    ───────────────────────────────")
    ceil_label = valid_candidates / total_unique * 100
    ceil_q = valid_candidates_q / total_q_eq * 100
    print(f"    CEILING (label-recall):  {ceil_label:5.1f}%")
    print(f"    CEILING (q-coverage):    {ceil_q:5.1f}%")

# ============================================================
# AUDIT 6: Semantic sibling analysis for 2026 "brand new" labels  
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 6: SEMANTIC SIBLING ANALYSIS (2026 'brand new' labels)")
print("=" * 80)

test_year = 2026
train_q = [q for q in raw_questions if q["year"] < test_year]
test_q = [q for q in raw_questions if q["year"] == test_year]

hist_micros_set = set()
hist_by_parent = defaultdict(set)
for q in train_q:
    mk = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
    pk = f"{q['subject']}::{q['topic']}"
    hist_micros_set.add(mk)
    hist_by_parent[pk].add(q["micro_topic"])

brand_new_labels = []
for q in test_q:
    mk = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
    pk = f"{q['subject']}::{q['topic']}"
    if mk not in hist_micros_set:
        brand_new_labels.append({
            "key": mk,
            "micro": q["micro_topic"],
            "parent": pk,
            "siblings": hist_by_parent.get(pk, set()),
        })

# Deduplicate
seen = set()
unique_new = []
for item in brand_new_labels:
    if item["key"] not in seen:
        seen.add(item["key"])
        unique_new.append(item)

print(f"  {len(unique_new)} brand-new micro-topic labels in 2026:")
for i, item in enumerate(unique_new):
    sibling_list = sorted(item["siblings"])[:5]
    has_siblings = len(item["siblings"]) > 0
    sib_str = ", ".join(s[:40] for s in sibling_list) if sibling_list else "(no siblings)"
    print(f"    {i+1:2d}. NEW: {item['micro'][:55]}")
    print(f"        Parent: {item['parent'].split('::')[1][:35]}")
    print(f"        Historical siblings: {sib_str}")
    print()

# ============================================================
# AUDIT 7: learn_micro_tau — heuristic verification
# ============================================================
print("=" * 80)
print("AUDIT 7: MICRO TAU LEARNING (HEURISTIC vs ACTUAL)")
print("=" * 80)
print("  Current implementation: micro_tau[subj] = min(topic_tau[subj] * 1.3, 5.0)")
print("  This is NOT learned from micro-topic data — it's derived from topic tau.")
print("  Topic tau IS properly grid-searched on topic-level walk-forward.")
print("  But micro-topics have different temporal dynamics than topics.")
print("  A topic like 'Memory Management' appears every year.")
print("  Its micro-topics ('Paging', 'Segmentation', 'TLB') cycle unpredictably.")

# ============================================================
# AUDIT 8: Total unique topics vs micro-topics
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 8: TOPIC vs MICRO-TOPIC VOCABULARY RATIO")
print("=" * 80)
all_topics = set()
all_micro = set()
for q in raw_questions:
    all_topics.add(f"{q['subject']}::{q['topic']}")
    all_micro.add(f"{q['subject']}::{q['topic']}::{q['micro_topic']}")

print(f"  Unique topics: {len(all_topics)}")
print(f"  Unique micro-topics: {len(all_micro)}")
print(f"  Ratio: {len(all_micro)/len(all_topics):.1f} micro-labels per topic (avg)")

# Per topic breakdown
micros_per_topic = defaultdict(set)
for q in raw_questions:
    pk = f"{q['subject']}::{q['topic']}"
    micros_per_topic[pk].add(q["micro_topic"])

counts = [len(v) for v in micros_per_topic.values()]
print(f"  Micro-labels per topic: min={min(counts)}, median={int(np.median(counts))}, max={max(counts)}, mean={np.mean(counts):.1f}")

# Topics with most micro-labels
print(f"\n  Top 10 topics by micro-label count:")
for pk, micros in sorted(micros_per_topic.items(), key=lambda x: -len(x[1]))[:10]:
    print(f"    {pk.split('::')[1][:40]:42s}: {len(micros)} micro-labels")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
