"""
Deep analysis of New Micro-Topic patterns across GATE history.
Goal: Determine the optimal number of New MT slots and the architecture to predict them.
"""
import json
from collections import defaultdict, Counter
import numpy as np

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ============================================================
# 1. How many NEW MTs appear each year?
# ============================================================
print("=" * 80)
print("SECTION 1: NEW MICRO-TOPIC COUNTS PER YEAR")
print("=" * 80)

seen_mts = set()
yearly_stats = {}

for year in range(2011, 2027):
    year_qs = [q for q in data if q['year'] == year]
    year_mts = set()
    for q in year_qs:
        mt_key = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        year_mts.add(mt_key)
    
    new_mts = year_mts - seen_mts
    old_mts = year_mts & seen_mts
    
    total = len(year_mts)
    n_new = len(new_mts)
    n_old = len(old_mts)
    pct_new = (n_new / total * 100) if total > 0 else 0
    
    yearly_stats[year] = {
        'total': total, 'new': n_new, 'old': n_old, 
        'pct_new': pct_new, 'new_mts': new_mts, 'old_mts': old_mts
    }
    
    seen_mts.update(year_mts)
    
    print(f"  {year}: {total:3d} unique MTs | {n_new:3d} NEW ({pct_new:5.1f}%) | {n_old:3d} OLD ({100-pct_new:5.1f}%)")

# Stats for test years only (2018-2026)
test_years = [y for y in range(2018, 2027)]
new_counts = [yearly_stats[y]['new'] for y in test_years]
new_pcts = [yearly_stats[y]['pct_new'] for y in test_years]

print(f"\n  --- Test Period (2018-2026) ---")
print(f"  New MT count: min={min(new_counts)}, max={max(new_counts)}, mean={np.mean(new_counts):.1f}, median={np.median(new_counts):.1f}")
print(f"  New MT %:     min={min(new_pcts):.1f}%, max={max(new_pcts):.1f}%, mean={np.mean(new_pcts):.1f}%, median={np.median(new_pcts):.1f}%")

# ============================================================
# 2. What SUBJECTS do new MTs come from?
# ============================================================
print("\n" + "=" * 80)
print("SECTION 2: WHICH SUBJECTS PRODUCE NEW MTs?")
print("=" * 80)

for year in test_years:
    new_mts = yearly_stats[year]['new_mts']
    subj_counts = Counter()
    for mt in new_mts:
        subj = mt.split("::")[0]
        subj_counts[subj] += 1
    
    print(f"\n  {year} ({len(new_mts)} new MTs):")
    for subj, cnt in subj_counts.most_common():
        print(f"    {subj[:35]:35s}: {cnt:2d} new MTs")

# ============================================================
# 3. What TOPICS do new MTs come from?
# ============================================================
print("\n" + "=" * 80)
print("SECTION 3: WHICH TOPICS PRODUCE NEW MTs?")
print("=" * 80)

topic_new_mt_count = defaultdict(int)  # How many times a topic produced a new MT
topic_total_appearances = defaultdict(int)  # How many years a topic appeared
topic_years_appeared = defaultdict(set)

for year in test_years:
    year_qs = [q for q in data if q['year'] == year]
    year_topics = set()
    for q in year_qs:
        tk = f"{q['subject']}::{q['topic']}"
        year_topics.add(tk)
    
    for tk in year_topics:
        topic_total_appearances[tk] += 1
        topic_years_appeared[tk].add(year)
    
    for mt in yearly_stats[year]['new_mts']:
        parts = mt.split("::")
        tk = f"{parts[0]}::{parts[1]}"
        topic_new_mt_count[tk] += 1

print("\n  Topics that FREQUENTLY produce new MTs (sorted by new MT count):")
for tk, cnt in sorted(topic_new_mt_count.items(), key=lambda x: x[1], reverse=True)[:25]:
    apps = topic_total_appearances[tk]
    rate = cnt / apps * 100
    print(f"    {tk[:50]:50s}: {cnt:2d} new MTs in {apps} appearances ({rate:.0f}% new-MT rate)")

# ============================================================
# 4. SYLLABUS GAP analysis - topics that haven't appeared recently
# ============================================================
print("\n" + "=" * 80)
print("SECTION 4: SYLLABUS GAP ANALYSIS (Last-Seen vs New-MT)")
print("=" * 80)

# For each new MT that appeared in year Y, how long had its TOPIC been absent?
gap_data = []
for year in test_years:
    for mt in yearly_stats[year]['new_mts']:
        parts = mt.split("::")
        subj, topic = parts[0], parts[1]
        tk = f"{subj}::{topic}"
        
        # Find last year this TOPIC appeared before this year
        prev_years = [q['year'] for q in data if q['year'] < year and q['subject'] == subj and q['topic'] == topic]
        if prev_years:
            last_seen = max(prev_years)
            gap = year - last_seen
        else:
            gap = -1  # Topic never seen before
        
        gap_data.append({'year': year, 'mt': mt, 'topic': tk, 'gap': gap})

# Analyze gaps
gaps_known = [d['gap'] for d in gap_data if d['gap'] > 0]
gaps_brand_new = [d for d in gap_data if d['gap'] == -1]

print(f"\n  Total new MTs analyzed: {len(gap_data)}")
print(f"  From known topics (gap > 0): {len(gaps_known)}")
print(f"  From brand-new topics (never seen): {len(gaps_brand_new)}")

if gaps_known:
    print(f"\n  Gap distribution (years since topic last appeared):")
    gap_counter = Counter(gaps_known)
    for g in sorted(gap_counter.keys()):
        pct = gap_counter[g] / len(gaps_known) * 100
        bar = "█" * int(pct / 2)
        print(f"    Gap={g:2d} years: {gap_counter[g]:3d} new MTs ({pct:5.1f}%) {bar}")

# ============================================================
# 5. How many new MTs should we predict?
# ============================================================
print("\n" + "=" * 80)
print("SECTION 5: OPTIMAL NUMBER OF NEW MT SLOTS")
print("=" * 80)

# If we predict N_new slots, what's the theoretical maximum recall?
# We need to know: of all new MTs, how many come from predictable patterns?

# Pattern 1: New MT from a topic that appeared 1 year ago (gap=1) 
# Pattern 2: New MT from a topic with gap 2-3 years
# Pattern 3: New MT from a topic with gap 4+ years (rotation)
# Pattern 4: Brand new topic entirely

for year in test_years:
    year_new = [d for d in gap_data if d['year'] == year]
    gap_1 = len([d for d in year_new if d['gap'] == 1])
    gap_2_3 = len([d for d in year_new if d['gap'] in [2, 3]])
    gap_4_plus = len([d for d in year_new if d['gap'] >= 4])
    brand_new = len([d for d in year_new if d['gap'] == -1])
    
    total = len(year_new)
    print(f"  {year}: {total:2d} new MTs -> Gap1: {gap_1:2d} | Gap2-3: {gap_2_3:2d} | Gap4+: {gap_4_plus:2d} | BrandNew: {brand_new:2d}")

# Average distribution
avg_total = np.mean([yearly_stats[y]['new'] for y in test_years])
avg_gap1 = np.mean([len([d for d in gap_data if d['year'] == y and d['gap'] == 1]) for y in test_years])
avg_gap23 = np.mean([len([d for d in gap_data if d['year'] == y and d['gap'] in [2, 3]]) for y in test_years])
avg_gap4p = np.mean([len([d for d in gap_data if d['year'] == y and d['gap'] >= 4]) for y in test_years])
avg_brand = np.mean([len([d for d in gap_data if d['year'] == y and d['gap'] == -1]) for y in test_years])

print(f"\n  --- AVERAGES (2018-2026) ---")
print(f"  Total new MTs:  {avg_total:.1f}")
print(f"  Gap=1 (recent): {avg_gap1:.1f} ({avg_gap1/avg_total*100:.1f}%)")
print(f"  Gap=2-3:        {avg_gap23:.1f} ({avg_gap23/avg_total*100:.1f}%)")
print(f"  Gap=4+:         {avg_gap4p:.1f} ({avg_gap4p/avg_total*100:.1f}%)")
print(f"  Brand new:      {avg_brand:.1f} ({avg_brand/avg_total*100:.1f}%)")

# ============================================================
# 6. Per-subject new MT rate 
# ============================================================
print("\n" + "=" * 80)
print("SECTION 6: PER-SUBJECT NEW MT PRODUCTION RATE")
print("=" * 80)

subj_new_total = defaultdict(int)
subj_total = defaultdict(int)
for year in test_years:
    for mt in yearly_stats[year]['new_mts']:
        subj = mt.split("::")[0]
        subj_new_total[subj] += 1
    year_qs = [q for q in data if q['year'] == year]
    for q in year_qs:
        mt_key = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        subj_total[q['subject']] += 1

print(f"\n  {'Subject':<40} {'New MTs':>8} {'Total Qs':>10} {'New MT Rate':>12}")
print("  " + "-" * 72)
for subj in sorted(subj_new_total.keys()):
    n = subj_new_total[subj]
    t = subj_total[subj]
    rate = n / t * 100 if t > 0 else 0
    print(f"  {subj:<40} {n:>8} {t:>10} {rate:>10.1f}%")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
