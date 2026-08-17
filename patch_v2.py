import re
with open("gate_apex_v10.py", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r"    def predict_micro_new\(self, target_year: int\) -> List\[dict\]:.*?(?=    # 10\.  Validator)", text, re.DOTALL)
if m:
    print(f"Found method. Length: {len(m.group(0))}")
else:
    print("Method not found.")
