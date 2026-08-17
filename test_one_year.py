import json
import numpy as np
from collections import defaultdict
from gate_apex_v10 import BestPredictor
import sys

with open("Q.json", "r", encoding="utf-8") as f:
    data = json.load(f)

processed_data = []
for q in data:
    processed_data.append({
        'subject': q['subject'], 'topic': q['topic'], 'micro': q['micro_topic'],
        'year': q['year'], 'count_inc': 1.0
    })

ty = 2026
train_q = [q for q in processed_data if q['year'] < ty]
test_q = [q for q in processed_data if q['year'] == ty]

pipeline = BestPredictor()
pipeline.train(train_q)
topic_preds = pipeline.predict_topics(target_year=ty)
micro_preds_old = pipeline.predict_micro(topic_preds, ty)  
micro_preds_new = pipeline.predict_micro_new(ty)

print("Old preds:", len(micro_preds_old))
print("New preds strictly >0.60:", len(micro_preds_new))
