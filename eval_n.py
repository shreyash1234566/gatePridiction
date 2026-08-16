import json
import numpy as np
from collections import defaultdict
from gate_apex_v10 import BestPredictor

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

processed_data = []
for q in data:
    processed_data.append({
        'subject': q['subject'],
        'topic': q['topic'],
        'micro': q['micro_topic'],
        'year': q['year'],
        'count_inc': 1.0
    })

def eval_at_n(ns):
    m_hits = {n: [] for n in ns}
    m_covs = {n: [] for n in ns}
    
    test_years = range(2018, 2027)
    
    for ty in test_years:
        train_q = [q for q in processed_data if q['year'] < ty]
        test_q = [q for q in processed_data if q['year'] == ty]
        
        # Initialize full pipeline exactly like main script
        pipeline = BestPredictor()
        
        # Train ML models
        pipeline.train(train_q)
        
        # Get REAL topic predictions
        topic_preds = pipeline.predict_topics(target_year=ty)
        
        # Get REAL micro predictions
        micro_preds = pipeline.predict_micro(topic_preds, ty)
        
        # Build ground truth
        act_micro = defaultdict(float)
        for q in test_q:
            # Main script preprocessing
            m = q.get('micro_topic', q.get('micro', ''))
            act_micro[f"{q['subject']}::{q['topic']}::{m}"] += 1
            
        # Build expansion map
        concept_to_raw = defaultdict(set)
        for q in train_q:
            m = q.get('micro_topic', q.get('micro', ''))
            concept = pipeline._get_canonical_concept(q['subject'], q['topic'], m)
            ck = f"{q['subject']}::{q['topic']}::{concept}"
            concept_to_raw[ck].add(f"{q['subject']}::{q['topic']}::{m}")
            
        # Expand predictions
        raw_preds = defaultdict(float)
        for m in micro_preds:
            concept = m.get('canonical_concept', m['micro_topic'])
            ck = f"{m['subject']}::{m['topic']}::{concept}"
            
            raw_labels = concept_to_raw.get(ck, {ck})
            score_per_raw = m['predicted_count'] / len(raw_labels) if raw_labels else m['predicted_count']
            
            for raw in raw_labels:
                raw_preds[raw] += score_per_raw
                
        # Sort by score descending
        sorted_raw = sorted(raw_preds.items(), key=lambda x: x[1], reverse=True)
        
        for n in ns:
            top_n = {k for k, v in sorted_raw[:n]}
            
            hits = sum(1 for k in act_micro if act_micro[k] > 0 and k in top_n)
            n_act = sum(1 for k in act_micro if act_micro[k] > 0)
            hit_r = hits / n_act * 100 if n_act else 0.0
            
            q_covered = sum(act_micro[k] for k in act_micro if k in top_n)
            total_q = sum(act_micro.values())
            cov_pct = (q_covered / total_q * 100) if total_q > 0 else 0.0
            
            m_hits[n].append(hit_r)
            m_covs[n].append(cov_pct)
            
    return {n: (np.mean(m_hits[n]), np.mean(m_covs[n])) for n in ns}

ns = list(range(180, 271, 10))
print("\nACTUAL PIPELINE PERFORMANCE - FINDING THE INFLECTION POINT")
print("-" * 75)
print(f"{'N':<10} | {'M_Hit %':<15} | {'Marginal Gain':<15} | {'M_Cov %':<15}")
print("-" * 75)
results = eval_at_n(ns)

prev_hit = None
for n in ns:
    hit, cov = results[n]
    gain = f"+{(hit - prev_hit):.1f}%" if prev_hit is not None else "N/A"
    print(f"{n:<10} | {hit:<15.1f} | {gain:<15} | {cov:<15.1f}")
    prev_hit = hit
