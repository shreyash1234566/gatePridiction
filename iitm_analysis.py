import json
from collections import defaultdict, Counter

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Organizing Institutes mapping
institutes = {
    2011: "IIT Madras",
    2012: "IIT Delhi",
    2013: "IIT Bombay",
    2014: "IIT Kharagpur",
    2015: "IIT Kanpur",
    2016: "IISc Bangalore",
    2017: "IIT Roorkee",
    2018: "IIT Guwahati",
    2019: "IIT Madras",
    2020: "IIT Delhi",
    2021: "IIT Bombay",
    2022: "IIT Kharagpur",
    2023: "IIT Kanpur",
    2024: "IISc Bangalore",
    2025: "IIT Roorkee",
    2026: "IIT Guwahati",
    2027: "IIT Madras"
}

by_year = defaultdict(list)
for q in data:
    by_year[q["year"]].append(q)

years = sorted(by_year.keys())

seen_mts = set()
yearly_new_mts = defaultdict(list)
yearly_all_mts = defaultdict(list)

for yr in years:
    qs = by_year[yr]
    for q in qs:
        mt = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        yearly_all_mts[yr].append(q)
        if mt not in seen_mts:
            yearly_new_mts[yr].append(q)
            seen_mts.add(mt)

print("="*80)
print("IIT MADRAS (2011, 2019) vs OTHER INSTITUTES ANALYSIS")
print("="*80)

# Compare IIT Madras years vs Others (Subject distribution for NEW MTs)
iitm_years = [2011, 2019]
other_years = [y for y in years if y not in iitm_years and y > 2011]

print("\n1. NEW MICRO-TOPICS BY SUBJECT (IITM vs Others)")
iitm_subj_new = Counter()
other_subj_new = Counter()

for yr in iitm_years:
    if yr == 2011: continue # Everything was new in 2011, skip it for "new MT" logic
    for q in yearly_new_mts[yr]:
        iitm_subj_new[q['subject']] += 1

for yr in other_years:
    for q in yearly_new_mts[yr]:
        other_subj_new[q['subject']] += 1

# Normalize to get average per year
iitm_avg = {k: v / 1.0 for k, v in iitm_subj_new.items()} # only 2019 has true "new"
other_avg = {k: v / len(other_years) for k, v in other_subj_new.items()}

all_subjs = set(iitm_avg.keys()) | set(other_avg.keys())
for subj in sorted(all_subjs):
    print(f"{subj:45s} | IITM avg: {iitm_avg.get(subj, 0):4.1f} | Other avg: {other_avg.get(subj, 0):4.1f}")


print("\n2. OVERALL QUESTION WEIGHTAGE (IITM vs Others)")
iitm_subj_all = Counter()
other_subj_all = Counter()

for yr in iitm_years:
    for q in yearly_all_mts[yr]:
        iitm_subj_all[q['subject']] += q.get('count_inc', 1.0)

for yr in other_years:
    for q in yearly_all_mts[yr]:
        other_subj_all[q['subject']] += q.get('count_inc', 1.0)

iitm_tot = sum(iitm_subj_all.values())
other_tot = sum(other_subj_all.values())

for subj in sorted(all_subjs):
    i_pct = iitm_subj_all.get(subj, 0) / iitm_tot * 100
    o_pct = other_subj_all.get(subj, 0) / other_tot * 100
    print(f"{subj:45s} | IITM wt: {i_pct:4.1f}% | Other wt: {o_pct:4.1f}% | Diff: {i_pct-o_pct:5.1f}%")

print("\n3. SPECIFIC TOPICS FAVORED BY IIT MADRAS (Top positive diff)")
iitm_topic_all = Counter()
other_topic_all = Counter()

for yr in iitm_years:
    for q in yearly_all_mts[yr]:
        iitm_topic_all[f"{q['subject']}::{q['topic']}"] += q.get('count_inc', 1.0)

for yr in other_years:
    for q in yearly_all_mts[yr]:
        other_topic_all[f"{q['subject']}::{q['topic']}"] += q.get('count_inc', 1.0)

diffs = {}
for topic in set(iitm_topic_all.keys()) | set(other_topic_all.keys()):
    i_pct = iitm_topic_all.get(topic, 0) / iitm_tot * 100
    o_pct = other_topic_all.get(topic, 0) / other_tot * 100
    diffs[topic] = i_pct - o_pct

for topic, diff in sorted(diffs.items(), key=lambda x: -x[1])[:10]:
    print(f"{topic:60s} | IITM bias: +{diff:.1f}%")

print("\n4. 2019 SPECIFIC NEW MTs INTRODUCED BY IIT MADRAS")
for q in yearly_new_mts[2019]:
    print(f" - {q['subject']} -> {q['topic']} -> {q['micro_topic']}")
