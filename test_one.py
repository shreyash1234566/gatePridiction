import sys, io
buf = io.StringIO(); old_stdout = sys.stdout; sys.stdout = buf
import json
from gate_apex_v10 import BestPredictor
with open("Q.json", "r", encoding="utf-8") as f: data = json.load(f)

processed_data = [{'subject': q['subject'], 'topic': q['topic'], 'micro': q['micro_topic'], 'year': q['year'], 'count_inc': 1.0} for q in data]
train_q = [q for q in processed_data if q['year'] < 2026]
pipeline = BestPredictor()
pipeline.train(train_q)
topic_preds = pipeline.predict_topics(target_year=2026)
concept_preds = pipeline.predict_micro(topic_preds, 2026)
micro_preds_old = pipeline.expand_and_rank_micro_topics(concept_preds, 2026)
sys.stdout = old_stdout
if len(micro_preds_old) > 0:
    print(f"Success! {len(micro_preds_old)} raw MTs scored by ML ranker.")
    print("Top 3:", micro_preds_old[:3])
