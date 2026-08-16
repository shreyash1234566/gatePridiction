import json
from collections import defaultdict
from gate_apex_v10 import BestPredictor, build_data

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# PREPROCESS data like in gate_apex_v10.py
processed_data = []
for q in data:
    processed_data.append({
        'subject': q['subject'],
        'topic': q['topic'],
        'micro': q['micro_topic'],
        'year': q['year'],
        'count_inc': 1.0
    })

train_q = [q for q in processed_data if q['year'] < 2026]
test_q = [q for q in processed_data if q['year'] == 2026]

pred = BestPredictor()
act_topic = defaultdict(float)
for q in test_q: 
    act_topic[f"{q['subject']}::{q['topic']}"] += 1
    
topic_preds = [{'subject': k.split('::')[0], 'topic': k.split('::')[1], 'predicted_count': v} for k,v in act_topic.items()]
pred.topic_data, pred.micro_data = build_data(train_q)
pred.learn_micro_tau_per_subject(pred.micro_data, [2026])
micro_preds = pred.predict_micro(topic_preds, 2026)

pred_micro = set()
concept_to_raw = defaultdict(set)
for q in train_q:
    concept = pred._get_canonical_concept(q['subject'], q['topic'], q['micro'])
    ck = f"{q['subject']}::{q['topic']}::{concept}"
    concept_to_raw[ck].add(f"{q['subject']}::{q['topic']}::{q['micro']}")
    
for m in micro_preds:
    concept = m.get('canonical_concept', m['micro_topic'])
    ck = f"{m['subject']}::{m['topic']}::{concept}"
    if ck in concept_to_raw: 
        pred_micro.update(concept_to_raw[ck])
    else: 
        pred_micro.add(ck)
        
print(f"\nPredicted raw MTs for 2026: {len(pred_micro)}")
print(f"Number of concepts predicted: {len(micro_preds)}")
