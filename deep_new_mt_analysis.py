import json
import numpy as np
from collections import defaultdict
from gate_apex_v10 import BestPredictor

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

processed_data = [{'subject': q['subject'], 'topic': q['topic'], 'micro': q['micro_topic'], 'year': q['year'], 'count_inc': 1.0} for q in data]
test_years = range(2018, 2027)

all_hits_scores = []
all_misses_scores = []
signal_correlations = {"s1": [], "s2": [], "s3": []}

for ty in test_years:
    train_q = [q for q in processed_data if q['year'] < ty]
    test_q = [q for q in processed_data if q['year'] == ty]
    
    # What are the actual new MTs in ty?
    train_seen = {f"{q['subject']}::{q['topic']}::{q['micro']}" for q in train_q}
    test_actual = {f"{q['subject']}::{q['topic']}::{q['micro']}" for q in test_q}
    actual_new_mts = test_actual - train_seen
    
    pipeline = BestPredictor()
    pipeline.train(train_q)
    
    # We need to hack predict_micro_new to return the raw candidates and their signals before sorting
    # Since we can't easily do it without rewriting, let's just re-implement the signals here identically
    
    # Build first_seen
    first_seen = {}
    micro_data = pipeline.micro_data
    for mk, d in micro_data.items():
        valid_years = [y for y, c in zip(d["years"], d["counts"]) if y < ty and c > 0]
        if valid_years: first_seen[mk] = min(valid_years)
        
    topic_new_mt_count = defaultdict(int)
    subj_new_mt_count = defaultdict(int)
    topic_appearances = defaultdict(set)
    topic_last_seen = {}
    
    for k, d in pipeline.topic_data.items():
        pk = f"{d['subject']}::{d['topic']}"
        valid_years = [y for y, c in zip(d["years"], d["counts"]) if y < ty and c > 0]
        if valid_years:
            for y in valid_years: topic_appearances[pk].add(y)
            topic_last_seen[pk] = max(valid_years)
            
    for mk, yr in first_seen.items():
        if yr >= 2011:
            parts = mk.split("::")
            subj, topic = parts[0], parts[1]
            topic_new_mt_count[f"{subj}::{topic}"] += 1
            subj_new_mt_count[subj] += 1
            
    subj_total_qs = defaultdict(float)
    for mk, d in micro_data.items():
        parts = mk.split("::")
        count = sum(c for y, c in zip(d["years"], d["counts"]) if y >= 2011 and y < ty)
        subj_total_qs[parts[0]] += count
        
    topic_rate = {}
    for pk in topic_appearances:
        apps = len(topic_appearances[pk])
        topic_rate[pk] = topic_new_mt_count[pk] / apps if apps > 0 else 0
        
    subj_rate = {}
    for s in subj_total_qs:
        subj_rate[s] = subj_new_mt_count[s] / subj_total_qs[s] if subj_total_qs[s] > 0 else 0
        
    max_t_rate = max(topic_rate.values()) if topic_rate else 1.0
    for pk in topic_rate: topic_rate[pk] /= (max_t_rate if max_t_rate > 0 else 1.0)
    
    with open("gate_syllabus.json", "r", encoding="utf-8") as f:
        syllabus = json.load(f)
        
    seen_labels = set()
    for mk in first_seen.keys():
        parts = mk.split("::")
        if len(parts) >= 3:
            norm_mt = parts[2].strip().lower()
            seen_labels.add(f"{parts[0]}::{parts[1]}::{norm_mt}")
            
    candidates = []
    for subj, topics in syllabus.items():
        for topic, mt_list in topics.items():
            pk = f"{subj}::{topic}"
            for mt in mt_list:
                norm_mt = mt.strip().lower()
                if f"{subj}::{topic}::{norm_mt}" not in seen_labels:
                    s1 = topic_rate.get(pk, 0.0)
                    s2 = subj_rate.get(subj, 0.0)
                    last_yr = topic_last_seen.get(pk, -1)
                    if last_yr > 0:
                        gap = ty - last_yr
                        if gap == 1: s3 = 1.0
                        elif gap in [2,3]: s3 = 0.5
                        else: s3 = 0.3
                    else:
                        s3 = 0.1
                        
                    score = 0.45 * s1 + 0.30 * s2 + 0.25 * s3
                    candidates.append({
                        "key": f"{subj}::{topic}::{mt}",
                        "s1": s1, "s2": s2, "s3": s3, "score": score,
                        "is_hit": 1 if f"{subj}::{topic}::{mt}" in actual_new_mts else 0
                    })
                    
    # Analysis per year
    for c in candidates:
        if c["is_hit"]: all_hits_scores.append(c)
        else: all_misses_scores.append(c)

print(f"Total True New MT Candidates that hit: {len(all_hits_scores)}")
print(f"Total True New MT Candidates that missed: {len(all_misses_scores)}")
if len(all_hits_scores) > 0:
    for sig in ["s1", "s2", "s3", "score"]:
        hit_mean = np.mean([c[sig] for c in all_hits_scores])
        miss_mean = np.mean([c[sig] for c in all_misses_scores])
        print(f"{sig} -> Hits avg: {hit_mean:.3f} | Misses avg: {miss_mean:.3f}")
