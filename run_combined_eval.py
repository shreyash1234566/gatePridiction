import json
import numpy as np
from collections import defaultdict
from gate_apex_v10 import BestPredictor
import sys

def run_main():
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

    n_old = 250
    n_new_list = [0, 5, 10, 15, 20]
    results_by_n_new = {n: {"hits": [], "covs": [], "actual_new": []} for n in n_new_list}
    
    test_years = range(2018, 2027)
    
    for ty in test_years:
        train_q = [q for q in processed_data if q['year'] < ty]
        test_q = [q for q in processed_data if q['year'] == ty]
        
        pipeline = BestPredictor()
        pipeline.train(train_q)
        topic_preds = pipeline.predict_topics(target_year=ty)
        
        # 1. Predict Concepts (Old)
        concept_preds = pipeline.predict_micro(topic_preds, ty)  
        
        # 2. Expand & Rank with ML (Old raw MTs)
        micro_preds_old = pipeline.expand_and_rank_micro_topics(concept_preds, target_year=ty)
        
        # 3. New MTs - tell it to max out at 20
        micro_preds_new = pipeline.predict_micro_new(ty, max_new=max(n_new_list))
        
        # Build ground truth
        act_micro = defaultdict(float)
        for q in test_q:
            m = q.get('micro_topic', q.get('micro', ''))
            act_micro[f"{q['subject']}::{q['topic']}::{m}"] += 1
            
        # Top 250 Old RAW MTs explicitly from our ML ranker
        top_old = micro_preds_old[:n_old]
        
        for n_new in n_new_list:
            actual_new_returned = micro_preds_new[:n_new]
            new_mt_keys = {f"{m['subject']}::{m['topic']}::{m['micro_topic']}" for m in actual_new_returned}
            
            top_combined = {f"{m['subject']}::{m['topic']}::{m['micro_topic']}" for m in top_old}.union(new_mt_keys)
            
            hits = sum(1 for k in act_micro if act_micro[k] > 0 and k in top_combined)
            n_act = sum(1 for k in act_micro if act_micro[k] > 0)
            hit_r = hits / n_act * 100 if n_act else 0.0
            
            q_covered = sum(act_micro[k] for k in act_micro if k in top_combined)
            total_q = sum(act_micro.values())
            cov_pct = (q_covered / total_q * 100) if total_q > 0 else 0.0
            
            results_by_n_new[n_new]["hits"].append(hit_r)
            results_by_n_new[n_new]["covs"].append(cov_pct)
            results_by_n_new[n_new]["actual_new"].append(len(actual_new_returned))

    print(f"\nRESULTS FOR ML-Ranked Old={n_old} + Filtered/Decayed New MTs:")
    for n_new in n_new_list:
        hit_mean = np.mean(results_by_n_new[n_new]["hits"])
        cov_mean = np.mean(results_by_n_new[n_new]["covs"])
        avg_act_new = np.mean(results_by_n_new[n_new]["actual_new"])
        print(f"N_new = {n_new:>2} (Avg Act: {avg_act_new:.1f}): M_Hit = {hit_mean:.1f}% | M_Cov = {cov_mean:.1f}%")

if __name__ == "__main__":
    run_main()
