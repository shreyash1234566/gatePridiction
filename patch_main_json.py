with open("gate_apex_v10.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """    predictions = final.predict_topics(2027)
    micro_predictions_old = final.predict_micro(predictions, 2027)
    micro_predictions_new = final.predict_micro_new(2027)

    micro_predictions = micro_predictions_old[:250] + micro_predictions_new"""

replacement = """    predictions = final.predict_topics(2027)
    concept_preds = final.predict_micro(predictions, 2027)
    
    # 7b. ML Ranked Raw Micro Topics (Strictly Top 250 Old)
    micro_predictions_old = final.expand_and_rank_micro_topics(concept_preds, 2027)
    
    # 8. New MT logic with Decay, capping at max 20
    micro_predictions_new = final.predict_micro_new(2027, max_new=20)

    micro_predictions = micro_predictions_old[:250] + micro_predictions_new"""

text = text.replace(target, replacement)

with open("gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Patched main() correctly.")
