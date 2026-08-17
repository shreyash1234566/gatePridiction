with open("E:/GATE PRIDICTION/gate_apex_v10.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("if True: # user requested raw microtopics\n            return self._predict_micro_legacy(topic_preds, target_year)\n        if not self.canonical_taxonomy:", "if True:\n            return self._predict_micro_legacy(topic_preds, target_year)")
text = text.replace("if True: # user requested raw microtopics\n", "")

with open("E:/GATE PRIDICTION/gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(text)
