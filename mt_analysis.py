"""
Deep analysis of micro-topic prediction:
1. How many MTs appear each year?
2. How many are NEW (never seen before)?
3. How many are OLD (repeats)?
4. What's the theoretical max M_Hit at different prediction counts?
5. What patterns exist in new MT selection?
"""
import json
from collections import defaultdict, Counter
import numpy as np

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Group by year
by_year = defaultdict(list)
for q in data:
    by_year[q["year"]].append(q)

years = sorted(by_year.keys())

print("=" * 90)
print("MICRO-TOPIC ANALYSIS: Old vs New, Prediction Coverage")
print("=" * 90)

# Track cumulative set of seen MTs
seen_mts = set()
yearly_stats = []

for yr in years:
    qs = by_year[yr]
    yr_mts = set()
    for q in qs:
        mt = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        yr_mts.add(mt)
    
    old_mts = yr_mts & seen_mts
    new_mts = yr_mts - seen_mts
    
    pct_old = len(old_mts) / len(yr_mts) * 100 if yr_mts else 0
    pct_new = len(new_mts) / len(yr_mts) * 100 if yr_mts else 0
    
    stat = {
        "year": yr,
        "total_q": len(qs),
        "unique_mts": len(yr_mts),
        "old_mts": len(old_mts),
        "new_mts": len(new_mts),
        "pct_old": pct_old,
        "pct_new": pct_new,
        "cumulative_seen": len(seen_mts),
    }
    yearly_stats.append(stat)
    
    print(f"\n  {yr}: {len(qs)} questions, {len(yr_mts)} unique MTs")
    print(f"    OLD (repeats):  {len(old_mts):3d} ({pct_old:.1f}%) — seen in previous years")
    print(f"    NEW (first time): {len(new_mts):3d} ({pct_new:.1f}%) — never seen before")
    print(f"    Cumulative pool: {len(seen_mts)} MTs available for prediction")
    
    seen_mts |= yr_mts

# For years 2018-2026, compute theoretical max hit rate at different prediction counts
print("\n\n" + "=" * 90)
print("THEORETICAL MAX HIT RATE at different prediction counts (2018-2026)")
print("=" * 90)

seen_mts = set()
for yr in years:
    if yr < 2018:
        for q in by_year[yr]:
            seen_mts.add(f"{q['subject']}::{q['topic']}::{q['micro_topic']}")
        continue
    
    yr_mts = set()
    for q in by_year[yr]:
        yr_mts.add(f"{q['subject']}::{q['topic']}::{q['micro_topic']}")
    
    old_mts = yr_mts & seen_mts
    
    # Count how many times each MT appeared in training data
    mt_counts = Counter()
    for prev_yr in years:
        if prev_yr >= yr:
            break
        for q in by_year[prev_yr]:
            mt_counts[f"{q['subject']}::{q['topic']}::{q['micro_topic']}"] += 1
    
    # Sort by frequency (most common first)
    ranked = sorted(mt_counts.keys(), key=lambda x: -mt_counts[x])
    
    print(f"\n  {yr}: {len(yr_mts)} actual MTs, {len(old_mts)} old / {len(yr_mts)-len(old_mts)} new")
    for top_k in [65, 100, 150, 180, 200, 250, 300]:
        predicted_set = set(ranked[:top_k])
        hits = predicted_set & yr_mts
        hit_rate = len(hits) / len(yr_mts) * 100
        # Also check OLD-only hit rate
        old_hits = predicted_set & old_mts
        old_hit_rate = len(old_hits) / len(old_mts) * 100 if old_mts else 0
        print(f"    Top-{top_k:3d}: Hit={hit_rate:5.1f}% ({len(hits)}/{len(yr_mts)}) "
              f"  Old-Hit={old_hit_rate:5.1f}% ({len(old_hits)}/{len(old_mts)})")
    
    seen_mts |= yr_mts

# Analyze patterns in NEW micro-topics
print("\n\n" + "=" * 90)
print("NEW MICRO-TOPIC PATTERNS")
print("=" * 90)

seen_mts = set()
new_mt_subjects = defaultdict(lambda: defaultdict(int))
new_mt_topics = defaultdict(lambda: defaultdict(int))

for yr in years:
    yr_mts = set()
    for q in by_year[yr]:
        mt = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        if mt not in seen_mts:
            new_mt_subjects[q['subject']][yr] += 1
            new_mt_topics[f"{q['subject']}::{q['topic']}"][yr] += 1
        yr_mts.add(mt)
    seen_mts |= yr_mts

print("\nNew MTs per subject (2018-2026):")
for subj in sorted(new_mt_subjects.keys()):
    counts = [new_mt_subjects[subj].get(yr, 0) for yr in range(2018, 2027)]
    avg = np.mean(counts)
    print(f"  {subj:50s}: {counts}  avg={avg:.1f}")

# Check how M_Hit is currently computed - what threshold?
print("\n\n" + "=" * 90)
print("CHECKING CURRENT PREDICTION OUTPUT")
print("=" * 90)
print("(Need to check gate_apex_v10.py for MICRO_PRED_TH and prediction count)")
