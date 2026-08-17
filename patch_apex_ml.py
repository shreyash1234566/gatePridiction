import re
with open("E:/GATE PRIDICTION/gate_apex_v10.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Clean up my previous hack in predict_micro
old_hack = """    def predict_micro(self, topic_preds: List[dict], target_year: int) -> List[dict]:
        return self._predict_micro_legacy(topic_preds, target_year)
        print(f"\n🔬 Micro‑topic predictions for {target_year} (Canonical Dirichlet) …")"""
new_hack = """    def predict_micro(self, topic_preds: List[dict], target_year: int) -> List[dict]:
        print(f"\n🔬 Micro‑topic predictions for {target_year} (Canonical Dirichlet) …")"""
code = code.replace(old_hack, new_hack)

# 2. Add train_micro_ml method and predict_raw_micro_topics method
class_end_pattern = r"(    def predict_micro_new\(self, target_year: int\) -> List\[dict\]:)"

ml_methods = """
    def train_micro_ml(self, target_year_mock: int = 2026):
        import xgboost as xgb
        # Build training data for micro-topics
        X_mt, y_mt = [], []
        
        # We will create examples for every year where we have history
        for mk, d in self.micro_data.items():
            if len(d["years"]) < 2:
                continue
            for i in range(1, len(d["years"])):
                curr_year = d["years"][i]
                past_years = d["years"][:i]
                past_counts = d["counts"][:i]
                
                features = self._extract_mt_features(past_years, past_counts, curr_year)
                X_mt.append(features)
                y_mt.append(1.0 if d["counts"][i] > 0 else 0.0)
                
                # add some negative samples? But we only have positive years in `years`.
                # We need to sample years it DIDN'T appear.
        
        # Actually, let's do a simpler approach: build a dataset of (micro_topic, year) for all years between min_yr and max_yr
        X_full, y_full = [], []
        min_yr, max_yr = 2011, max([max(d["years"]) for d in self.micro_data.values()])
        for mk, d in self.micro_data.items():
            first_yr = d["years"][0]
            for yr in range(first_yr + 1, max_yr + 1):
                # find history before yr
                past_years = [y for y in d["years"] if y < yr]
                past_counts = [d["counts"][idx] for idx, y in enumerate(d["years"]) if y < yr]
                if not past_years:
                    continue
                features = self._extract_mt_features(past_years, past_counts, yr)
                X_full.append(features)
                target = 1.0 if yr in d["years"] and d["counts"][d["years"].index(yr)] > 0 else 0.0
                y_full.append(target)
                
        if len(X_full) > 0:
            self.mt_ml_model = xgb.XGBRegressor(n_estimators=50, max_depth=3, learning_rate=0.05, objective='reg:squarederror')
            self.mt_ml_model.fit(X_full, y_full)
        else:
            self.mt_ml_model = None

    def _extract_mt_features(self, past_years, past_counts, curr_year):
        apps = len(past_years)
        last_gap = curr_year - past_years[-1]
        sum_c = sum(past_counts)
        apps_3y = sum(1 for y in past_years if curr_year - y <= 3)
        return [apps, last_gap, sum_c, apps_3y]

    def expand_and_rank_micro_topics(self, concept_preds: List[dict], target_year: int) -> List[dict]:
        '''Takes concept predictions, expands them to raw labels, scores them with ML, and returns top raw MTs.'''
        raw_candidates = []
        concept_to_raw = defaultdict(list)
        
        for mk, d in self.micro_data.items():
            valid_years = [y for y, c in zip(d["years"], d["counts"]) if y < target_year and c > 0]
            if not valid_years:
                continue
            pk = f"{d['subject']}::{d['topic']}"
            concept = self._get_canonical_concept(d["subject"], d["topic"], d["micro"])
            ck = f"{pk}::{concept}"
            concept_to_raw[ck].append({
                "micro": d["micro"],
                "subject": d["subject"],
                "topic": d["topic"],
                "features": self._extract_mt_features(valid_years, [c for y, c in zip(d["years"], d["counts"]) if y < target_year and c > 0], target_year)
            })
            
        for cp in concept_preds:
            ck = f"{cp['subject']}::{cp['topic']}::{cp['canonical_concept']}"
            raws = concept_to_raw.get(ck, [])
            if not raws:
                continue
                
            # ML scoring
            X_infer = [r["features"] for r in raws]
            if hasattr(self, 'mt_ml_model') and self.mt_ml_model is not None:
                ml_scores = self.mt_ml_model.predict(X_infer)
            else:
                ml_scores = [r["features"][0] for r in raws] # fallback to raw frequency
                
            ml_scores = [max(0.01, float(s)) for s in ml_scores]
            total_ml = sum(ml_scores)
            
            for r, ml_val in zip(raws, ml_scores):
                # Portion of the concept's predicted count according to ML score
                portion = ml_val / total_ml if total_ml > 0 else (1.0 / len(raws))
                raw_count = cp["predicted_count"] * portion
                
                raw_candidates.append({
                    "subject": r["subject"],
                    "topic": r["topic"],
                    "micro_topic": r["micro"],
                    "canonical_concept": cp["canonical_concept"],
                    "predicted_count": raw_count,
                    "ml_prob": ml_val,
                    "confidence": cp.get("confidence", 50)
                })
                
        # Consolidate exact duplicates if any
        final_map = {}
        for rc in raw_candidates:
            key = f"{rc['subject']}::{rc['topic']}::{rc['micro_topic']}"
            if key not in final_map:
                final_map[key] = rc
            else:
                final_map[key]["predicted_count"] += rc["predicted_count"]
                
        result = list(final_map.values())
        result.sort(key=lambda x: x["predicted_count"], reverse=True)
        return result

"""

code = re.sub(class_end_pattern, ml_methods + r"\1", code)

# 3. Add to train method
train_pattern = r"        # Stack features\n"
train_ml = """        self.train_micro_ml()
        # Stack features\n"""
code = code.replace("        # Stack features\n", train_ml)

with open("E:/GATE PRIDICTION/gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Patched ML into apex")
