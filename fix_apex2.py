with open("E:/GATE PRIDICTION/gate_apex_v10.py", "r", encoding="utf-8") as f:
    text = f.read()

old_block = """    def predict_micro(self, topic_preds: List[dict], target_year: int) -> List[dict]:
        print(f"\n🔬 Micro‑topic predictions for {target_year} (Canonical Dirichlet) …")
        parent_quota = {f"{p['subject']}::{p['topic']}": p["predicted_count"] for p in topic_preds}

        if not self.canonical_taxonomy:
            return self._predict_micro_legacy(topic_preds, target_year)"""

new_block = """    def predict_micro(self, topic_preds: List[dict], target_year: int) -> List[dict]:
        # User requested explicitly to predict raw microtopics, not concepts
        return self._predict_micro_legacy(topic_preds, target_year)

        print(f"\n🔬 Micro‑topic predictions for {target_year} (Canonical Dirichlet) …")
        parent_quota = {f"{p['subject']}::{p['topic']}": p["predicted_count"] for p in topic_preds}

        if not self.canonical_taxonomy:
            return self._predict_micro_legacy(topic_preds, target_year)"""

text = text.replace(old_block, new_block)

old_new = """        candidates.sort(key=lambda x: x["score"], reverse=True)
        top_40 = candidates[:40]"""

new_new = """        candidates.sort(key=lambda x: x["score"], reverse=True)
        # Apply high confidence filter: score >= 0.60
        high_conf = [c for c in candidates if c["score"] >= 0.60]
        # But allow at least some if they are really high, max 40
        top_40 = high_conf[:40]"""

text = text.replace(old_new, new_new)

with open("E:/GATE PRIDICTION/gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(text)

