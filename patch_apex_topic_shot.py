import re

with open('gate_apex_v10.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace:
#             # Micro predictions (snapshot)
#             orig_micro = self.pred.micro_data
#             self.pred.micro_data = md_snap
#             buf2 = io.StringIO()

old_block = """            # Micro predictions (snapshot)
            orig_micro = self.pred.micro_data
            self.pred.micro_data = md_snap
            buf2 = io.StringIO()"""

new_block = """            # Micro predictions (snapshot)
            orig_micro = self.pred.micro_data
            orig_topic = self.pred.topic_data
            self.pred.micro_data = md_snap
            self.pred.topic_data = td_snap
            buf2 = io.StringIO()"""

code = code.replace(old_block, new_block)

# Replace:
#             finally:
#                 sys.stdout = sys.__stdout__
#             self.pred.micro_data = orig_micro
# 
#             # Combine Old (250) + New (40) MTs
#             # First, fetch New MT predictions
#             buf3 = io.StringIO()
#             sys.stdout = buf3
#             try:
#                 micro_preds_new = self.pred.predict_micro_new(ty)
#             finally:
#                 sys.stdout = sys.__stdout__

old_block2 = """            finally:
                sys.stdout = sys.__stdout__
            self.pred.micro_data = orig_micro

            # Combine Old (250) + New (40) MTs
            # First, fetch New MT predictions
            buf3 = io.StringIO()
            sys.stdout = buf3
            try:
                micro_preds_new = self.pred.predict_micro_new(ty)
            finally:
                sys.stdout = sys.__stdout__"""

new_block2 = """            finally:
                sys.stdout = sys.__stdout__
            
            # Combine Old (250) + New (40) MTs
            # First, fetch New MT predictions
            buf3 = io.StringIO()
            sys.stdout = buf3
            try:
                micro_preds_new = self.pred.predict_micro_new(ty)
            finally:
                sys.stdout = sys.__stdout__
                
            self.pred.micro_data = orig_micro
            self.pred.topic_data = orig_topic"""

code = code.replace(old_block2, new_block2)

# Also fix the Seen Labels logic to use the full key
old_seen = """        seen_labels_normalized = set()
        for mk in first_seen.keys():
            parts = mk.split("::")
            if len(parts) >= 3:
                seen_labels_normalized.add(norm_topic(parts[2]).lower())"""

new_seen = """        seen_labels_normalized = set()
        for mk in first_seen.keys():
            parts = mk.split("::")
            if len(parts) >= 3:
                # Store full subject::topic::normalized_micro to avoid global exclusion
                seen_labels_normalized.add(f"{parts[0]}::{parts[1]}::{norm_topic(parts[2]).lower()}")"""

code = code.replace(old_seen, new_seen)

old_check = """                    norm_mt = norm_topic(mt).lower()
                    if norm_mt not in seen_labels_normalized:"""

new_check = """                    norm_mt = norm_topic(mt).lower()
                    if f"{subj}::{topic}::{norm_mt}" not in seen_labels_normalized:"""

code = code.replace(old_check, new_check)

with open('gate_apex_v10.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched gate_apex_v10.py successfully.")
