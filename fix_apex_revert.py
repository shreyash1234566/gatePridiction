with open("E:/GATE PRIDICTION/gate_apex_v10.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "return self._predict_micro_legacy(topic_preds, target_year)" in line and "User requested" not in line and "def predict_micro" not in line:
        pass # we only want to drop the ONE extra early return
        
# Just do string replace robustly
text = "".join(lines)
import re
text = re.sub(r'def predict_micro\(self, topic_preds: List\[dict\], target_year: int\) -> List\[dict\]:\n\s+return self\._predict_micro_legacy\(topic_preds, target_year\)\n', 'def predict_micro(self, topic_preds: List[dict], target_year: int) -> List[dict]:\n', text)
with open("E:/GATE PRIDICTION/gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(text)
