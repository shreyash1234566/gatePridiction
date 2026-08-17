#!/usr/bin/env python3
"""
GATE 2027 FUSION PREDICTION SYSTEM v9.0
=======================================
Evidence-driven hybrid of Elite v3.4, Ultimate v8.0, and Best v8.0.

Design goals:
    1. Keep topic-level stability from hard quota normalization.
    2. Improve micro recall with EMA + per-subject tau decay.
    3. Preserve calibration reliability via isotonic + blending.
    4. Use fair benchmark defaults (2018-2026) and reproducible knobs.
"""

from __future__ import annotations

import json
import os
import sys
import io
import itertools
import re
import warnings
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ----------------------------------------------------------------------
# 1.  Optional ML imports (graceful degradation)
# ----------------------------------------------------------------------
try:
    from sklearn.ensemble import (
        RandomForestRegressor, ExtraTreesRegressor,
        StackingRegressor, HistGradientBoostingRegressor
    )
    from sklearn.linear_model import BayesianRidge
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import TimeSeriesSplit, cross_val_predict
    from sklearn.isotonic import IsotonicRegression
    SKLEARN = True
except ImportError:
    SKLEARN = False
    print("⚠️  sklearn not available – fallback mode")

try:
    import xgboost as xgb
    XGBOOST = True
except ImportError:
    XGBOOST = False

try:
    import lightgbm as lgb
    LIGHTGBM = True
except ImportError:
    LIGHTGBM = False

try:
    from scipy import stats
    SCIPY = True
except ImportError:
    SCIPY = False

# ----------------------------------------------------------------------
# 2.  Constants – exact subject names from Q.json
# ----------------------------------------------------------------------
TOTAL_GATE_QUESTIONS = 65

SECTION_DISTRIBUTION = {
    "General Aptitude":                      10,
    "Programming and Data Structures":        8,
    "Engineering Mathematics":                5,
    "Operating Systems":                      6,
    "Computer Networks":                      5,
    "Databases":                              5,
    "Discrete Mathematics":                   5,
    "Computer Organization and Architecture": 5,
    "Theory of Computation":                  5,
    "Compiler Design":                        4,
    "Digital Logic":                          4,
    "Algorithms":                             3,
}
assert sum(SECTION_DISTRIBUTION.values()) == TOTAL_GATE_QUESTIONS

VALID_SUBJECTS = set(SECTION_DISTRIBUTION.keys())

MULTI_PAPER_YEARS = {2014: 3, 2015: 3, 2016: 2, 2021: 2, 2024: 2, 2025: 2, 2026: 2}

ERA_WEIGHTS = {
    "ancient":    0.05,   # < 2011
    "structural": 0.30,   # 2011-2013
    "cbt_stable": 0.65,   # 2014-2020
    "msq_era":    0.85,   # 2021-2022
    "current":    1.00,   # 2023+
}

# Core topics (used as feature & fallback)
CORE_TOPICS = {
    "General Aptitude": [
        "Quantitative Aptitude", "Verbal Ability",
        "Logical and Analytical Reasoning", "Spatial Aptitude"],
    "Programming and Data Structures": [
        "Programming in C", "Trees", "Arrays, Stacks, Queues, Linked Lists",
        "Graphs (Data Structure Representation)", "Recursion", "Hashing"],
    "Engineering Mathematics": [
        "Linear Algebra", "Probability and Statistics", "Calculus"],
    "Operating Systems": [
        "Memory Management", "CPU Scheduling",
        "Inter-Process Communication and Synchronization",
        "Deadlocks", "Process Management", "File Systems", "Virtual Memory"],
    "Computer Networks": [
        "Network Layer and IP Addressing", "Data Link Layer",
        "Transport Layer", "Application Layer Protocols", "Network Security"],
    "Databases": [
        "Transactions and Concurrency Control",
        "Functional Dependencies and Normalization",
        "Relational Model and Relational Algebra", "SQL",
        "File Organization and Indexing"],
    "Discrete Mathematics": [
        "Graph Theory", "Propositional and First-Order Logic",
        "Combinatorics", "Sets, Relations, Functions", "Algebraic Structures"],
    "Computer Organization and Architecture": [
        "Memory Hierarchy", "Instruction Pipelining",
        "Machine Instructions and Addressing Modes",
        "I/O Interface", "ALU, Data-Path and Control Unit"],
    "Theory of Computation": [
        "Regular Languages and Finite Automata",
        "Turing Machines and Decidability",
        "Context-Free Languages", "Closure and Decision Properties"],
    "Compiler Design": [
        "Syntax Analysis (Parsing)", "Code Optimization",
        "Semantic Analysis and Intermediate Code",
        "Lexical Analysis", "Runtime Environments"],
    "Digital Logic": [
        "Number Systems and Computer Arithmetic", "Boolean Algebra",
        "Sequential Circuits", "Combinational Circuits", "Minimization"],
    "Algorithms": [
        "Asymptotic Analysis", "Graph Algorithms",
        "Searching and Sorting", "Computational Complexity",
        "Algorithm Design: Dynamic Programming",
        "Algorithm Design: Greedy", "Algorithm Design: Divide and Conquer"],
}

# Topic normalization (merge variants)
TOPIC_NORM = {
    "Probability and Statistics": "Probability and Statistics",
    "Probability Distribution": "Probability and Statistics",
    "Random Variables": "Probability and Statistics",
    "Conditional Probability": "Probability and Statistics",
    "Bayes Theorem": "Probability and Statistics",
    "Bayes' Theorem": "Probability and Statistics",
    "Expected Value": "Probability and Statistics",
    "IP Header": "Network Layer and IP Addressing",
    "IP Addressing": "Network Layer and IP Addressing",
    "IPv4": "Network Layer and IP Addressing",
    "Subnetting": "Network Layer and IP Addressing",
    "CIDR": "Network Layer and IP Addressing",
    "Programming in C": "Programming in C",
    "C Programming / Pointers": "Programming in C",
    "C Pointers": "Programming in C",
    "Pointers": "Programming in C",
    "Pointers and Arrays": "Programming in C",
    "Memory Hierarchy": "Memory Hierarchy",
    "Cache Mapping": "Memory Hierarchy",
    "Cache": "Memory Hierarchy",
    "Page Replacement": "Virtual Memory",
    "Paging & Memory Management": "Memory Management",
    "Page Table": "Virtual Memory",
    "Demand Paging": "Virtual Memory",
    "Graph Theory": "Graph Theory",
    "BFS": "Graph Algorithms",
    "DFS": "Graph Algorithms",
    "Minimum Spanning Trees": "Minimum Spanning Tree",
    "MST": "Minimum Spanning Tree",
    "Syntax Analysis": "Syntax Analysis (Parsing)",
    "Parsing / Syntax Analysis": "Syntax Analysis (Parsing)",
    "LL Parsing": "Syntax Analysis (Parsing)",
    "LR Parsing": "Syntax Analysis (Parsing)",
    "Deadlocks": "Deadlocks",
    "Deadlock Conditions": "Deadlocks",
    "Binary Trees": "Trees",
    "Tree Traversal": "Trees",
    "Normal Forms": "Functional Dependencies and Normalization",
    "1NF": "Functional Dependencies and Normalization",
    "2NF": "Functional Dependencies and Normalization",
    "3NF": "Functional Dependencies and Normalization",
    "BCNF": "Functional Dependencies and Normalization",
}

def norm_topic(t: str) -> str:
    return TOPIC_NORM.get(t.strip(), t.strip()) if t else t

# ----------------------------------------------------------------------
# 3.  Environment‑controllable hyperparameters (Phase A tuning)
# ----------------------------------------------------------------------
def _ef(name: str, default: float, lo: Optional[float] = None, hi: Optional[float] = None) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        v = float(raw)
    except ValueError:
        return default
    if lo is not None:
        v = max(lo, v)
    if hi is not None:
        v = min(hi, v)
    return v

def _eb(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "y", "on"}

# Topic knobs
MIN_CONF_THRESHOLD   = _ef("GATE_MIN_CONF",     0.05, 0.0, 1.0)
NORM_BLEND           = _ef("GATE_BLEND",        0.85, 0.0, 1.0)
CONF_BLEND           = _ef("GATE_CONF_BLEND",   0.30, 0.0, 1.0)
TOPIC_TAU            = _ef("GATE_TOPIC_TAU",    3.0,  0.5, 10.0)
TOPIC_HIT_TH         = _ef("GATE_TOPIC_HIT",   0.25, 0.0, 5.0)

# Micro knobs – canonical Dirichlet model
MICRO_PRED_TH        = _ef("GATE_MICRO_TH",     0.10, 0.0, 5.0)    # single threshold: output AND evaluation
DIRICHLET_KAPPA      = _ef("GATE_KAPPA",        1.0,  0.01, 50.0)  # prior strength
DIRICHLET_DELTA      = _ef("GATE_DELTA",        0.85, 0.01, 0.999) # recency discount
OTHER_PRIOR_FRAC     = _ef("GATE_OTHER_FRAC",   0.10, 0.01, 0.50)  # prior mass for OTHER bucket

# Legacy micro knobs (kept for backward compat / fallback)
MICRO_TAU            = _ef("GATE_MICRO_TAU",    4.0,  0.5, 12.0)
MICRO_EMA_ALPHA      = _ef("GATE_MICRO_EMA",    0.70, 0.1, 0.99)
MICRO_HIT_TH         = MICRO_PRED_TH   # unified: same threshold
MICRO_MIN_PRED       = MICRO_PRED_TH   # unified: same threshold
MIN_APPEARANCES      = 2               # used by topic predictor (do not remove)
MIN_LAST_SEEN        = 2016            # used by topic predictor (do not remove)

TAU_GRID = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
TARGET_YEAR_FOR_TAU  = 2027
TAU_RECENCY_SCALE    = 3.0
KAPPA_GRID = [0.3, 0.5, 1.0, 2.0, 3.0, 5.0]
DELTA_GRID = [0.6, 0.7, 0.8, 0.85, 0.9, 0.95]

# Feature count (55)
FEATURE_DIM = 55

def get_knobs() -> dict:
    return {
        "min_conf": MIN_CONF_THRESHOLD,
        "blend": NORM_BLEND,
        "conf_blend": CONF_BLEND,
        "topic_tau": TOPIC_TAU,
        "topic_hit": TOPIC_HIT_TH,
        "micro_tau": MICRO_TAU,
        "micro_ema": MICRO_EMA_ALPHA,
        "micro_hit": MICRO_HIT_TH,
        "micro_min_pred": MICRO_MIN_PRED,
    }

def set_knobs(**kw) -> dict:
    global MIN_CONF_THRESHOLD, NORM_BLEND, CONF_BLEND, TOPIC_TAU, TOPIC_HIT_TH
    global MICRO_TAU, MICRO_EMA_ALPHA, MICRO_HIT_TH, MICRO_MIN_PRED
    prev = get_knobs()
    def clip(v, lo, hi):
        return float(np.clip(v, lo, hi))
    if "min_conf" in kw:
        MIN_CONF_THRESHOLD = clip(kw["min_conf"], 0.0, 1.0)
    if "blend" in kw:
        NORM_BLEND = clip(kw["blend"], 0.0, 1.0)
    if "conf_blend" in kw:
        CONF_BLEND = clip(kw["conf_blend"], 0.0, 1.0)
    if "topic_tau" in kw:
        TOPIC_TAU = clip(kw["topic_tau"], 0.5, 10.0)
    if "topic_hit" in kw:
        TOPIC_HIT_TH = clip(kw["topic_hit"], 0.0, 5.0)
    if "micro_tau" in kw:
        MICRO_TAU = clip(kw["micro_tau"], 0.5, 12.0)
    if "micro_ema" in kw:
        MICRO_EMA_ALPHA = clip(kw["micro_ema"], 0.1, 0.99)
    if "micro_hit" in kw:
        MICRO_HIT_TH = clip(kw["micro_hit"], 0.0, 5.0)
    if "micro_min_pred" in kw:
        MICRO_MIN_PRED = clip(kw["micro_min_pred"], 0.0, 1.0)
    return prev

# ----------------------------------------------------------------------
# 4.  Utilities
# ----------------------------------------------------------------------
def era_weight(year: int) -> float:
    if year < 2011:   return ERA_WEIGHTS["ancient"]
    if year <= 2013:  return ERA_WEIGHTS["structural"]
    if year <= 2020:  return ERA_WEIGHTS["cbt_stable"]
    if year <= 2022:  return ERA_WEIGHTS["msq_era"]
    return ERA_WEIGHTS["current"]

def ema(counts: List[float], alpha: float) -> float:
    """Exponential moving average (smoothing)."""
    if not counts:
        return 0.0
    e = float(counts[0])
    for c in counts[1:]:
        e = alpha * float(c) + (1 - alpha) * e
    return e

# ----------------------------------------------------------------------
# 5.  Data loading (exact subject names)
# ----------------------------------------------------------------------
def load_data(path: str = "Q.json", verbose: bool = True) -> List[dict]:
    print(f"\n📂 Loading {path} …")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raw = [raw]

    processed = []
    skipped = 0
    for q in raw:
        subj = (q.get("subject") or "").strip()
        topic = norm_topic((q.get("topic") or "").strip())
        micro = norm_topic((q.get("micro_topic") or topic).strip())
        try:
            year = int(q["year"])
        except (KeyError, ValueError):
            skipped += 1
            continue

        if subj not in VALID_SUBJECTS:
            skipped += 1
            continue
        if not topic:
            topic = subj

        np_ = MULTI_PAPER_YEARS.get(year, 1)
        processed.append({
            "year": year,
            "subject": subj,
            "topic": topic,
            "micro": micro,
            "n_papers": np_,
            "count_inc": 1.0 / np_,   # per‑paper normalised count
            "era_wt": era_weight(year),
        })

    if verbose:
        years = Counter(q["year"] for q in processed)
        subjs = Counter(q["subject"] for q in processed)
        print(f"   ✓ {len(processed)} questions ({skipped} skipped)")
        print(f"   Years: {sorted(years.keys())}")
        print("\n   Subject distribution:")
        for s in VALID_SUBJECTS:
            print(f"      {s[:42]:42s}: {subjs.get(s, 0):4d}")
    return processed

# ----------------------------------------------------------------------
# 6.  Build topic_data and micro_data (per‑paper normalised)
# ----------------------------------------------------------------------
def build_data(questions: List[dict]) -> Tuple[dict, dict]:
    topic_data = {}
    micro_data = {}

    for q in questions:
        s, t, m, y, w = q["subject"], q["topic"], q["micro"], q["year"], q["count_inc"]

        tk = f"{s}::{t}"
        if tk not in topic_data:
            topic_data[tk] = {"years": [], "yc": defaultdict(float), "subject": s, "topic": t}
        topic_data[tk]["years"].append(y)
        topic_data[tk]["yc"][y] += w

        mk = f"{s}::{t}::{m}"
        if mk not in micro_data:
            micro_data[mk] = {"years": [], "yc": defaultdict(float), "subject": s, "topic": t, "micro": m}
        micro_data[mk]["years"].append(y)
        micro_data[mk]["yc"][y] += w

    # Determine global year range for zero-filling
    all_years_seen = set()
    for q in questions:
        all_years_seen.add(q["year"])
    full_year_range = sorted(all_years_seen)

    for store in (topic_data, micro_data):
        for k in store:
            appeared_years = sorted(set(store[k]["years"]))
            # Zero-fill: include every year from first appearance to last
            first_yr = appeared_years[0]
            last_yr = appeared_years[-1]
            filled_years = [y for y in full_year_range if first_yr <= y <= last_yr]
            store[k]["years"] = filled_years
            store[k]["counts"] = [store[k]["yc"].get(y, 0.0) for y in filled_years]
            del store[k]["yc"]

    return topic_data, micro_data

# ----------------------------------------------------------------------
# 7.  Feature engineering (55 features – Elite v3.4 proven set)
# ----------------------------------------------------------------------
def extract_features(
    d: dict,
    all_td: dict,
    target_year: int,
    tau_map: Optional[Dict[str, float]] = None,
) -> np.ndarray:
    years = d["years"]
    counts = np.array(d["counts"], dtype=float)
    weights = np.array([era_weight(y) for y in years])
    n = len(counts)

    if n == 0:
        return np.zeros(FEATURE_DIM)

    feats = []

    # ---- Temporal (15) -------------------------------------------------
    w_mean = float(np.average(counts, weights=weights))
    recent_mean = float(np.mean(counts[-3:])) if n >= 3 else w_mean
    std_dev = float(np.std(counts)) if n > 1 else 0.0
    feats.extend([w_mean, recent_mean, std_dev])

    slope = r2 = momentum = 0.0
    if n >= 3:
        x = np.arange(n, dtype=float)
        cf = np.polyfit(x, counts, 1, w=weights)
        slope = float(cf[0])
        yp = np.polyval(cf, x)
        sst = float(np.sum((counts - counts.mean())**2))
        r2 = float(1 - np.sum((counts - yp)**2) / sst) if sst > 0 else 0.0
        momentum = float(counts[-1] - counts[-2]) if n >= 2 else 0.0
    feats.extend([slope, r2, momentum])

    for alpha in [0.3, 0.5, 0.7, 0.85, 0.95]:
        w = np.array([alpha**i for i in range(n)][::-1])
        feats.append(float(np.sum(counts * w) / w.sum()))

    accel = accel_std = 0.0
    if n >= 3:
        diffs = np.diff(counts)
        accel = float(np.mean(np.diff(diffs))) if len(diffs) > 1 else 0.0
        accel_std = float(np.std(np.diff(diffs))) if len(diffs) > 1 else 0.0
    feats.extend([accel, accel_std])

    tau = (tau_map or {}).get(d.get("subject", ""), TOPIC_TAU)
    last_seen = max(years)
    years_since = target_year - last_seen
    feats.extend([float(years_since), float(np.exp(-years_since / tau))])

    # ---- Statistical (10) ----------------------------------------------
    feats.extend([
        float(counts.min()), float(counts.max()),
        float(counts.max() - counts.min()),
        float(np.percentile(counts, 25)) if n >= 4 else float(counts.min()),
        float(np.percentile(counts, 75)) if n >= 4 else float(counts.max()),
    ])
    cv = std_dev / w_mean if w_mean > 0 else 0.0
    iqr = float(np.percentile(counts, 75) - np.percentile(counts, 25)) if n >= 4 else std_dev
    var = float(np.var(counts))
    skew = kurt = 0.0
    if SCIPY and n >= 4:
        skew = float(stats.skew(counts))
        kurt = float(stats.kurtosis(counts))
    feats.extend([cv, iqr, var, skew, kurt])

    # ---- Era‑based (5) ------------------------------------------------
    era_ranges = [(2011, 2013), (2014, 2020), (2021, 2022), (2023, 2099)]
    era_avgs = []
    for lo, hi in era_ranges:
        v = [c for y, c in zip(years, counts) if lo <= y <= hi]
        era_avgs.append(float(np.mean(v)) if v else 0.0)
    era_trans = era_avgs[-1] - era_avgs[-2] if len(era_avgs) >= 2 else 0.0
    feats.extend(era_avgs + [era_trans])

    # ---- Consistency (5) ----------------------------------------------
    span = max(years) - min(years) + 1 if n > 1 else 1
    appear_rate = n / span
    max_consec = 0
    cur = 0
    for i in range(1, n):
        if years[i] - years[i-1] == 1:
            cur += 1
            max_consec = max(max_consec, cur)
        else:
            cur = 0
    gap_mean = float(np.mean(np.diff(years))) if n > 1 else 0.0
    gap_std = float(np.std(np.diff(years))) if n > 1 else 0.0
    feats.extend([appear_rate, float(n), float(max_consec), gap_mean, gap_std])

    # ---- Subject context (7) ------------------------------------------
    subj = d["subject"]
    topic = d["topic"]
    is_core = float(topic in CORE_TOPICS.get(subj, []))
    quota = SECTION_DISTRIBUTION.get(subj, 5) / TOTAL_GATE_QUESTIONS
    n_topics = len([k for k in all_td if all_td[k]["subject"] == subj])
    topic_share = 1.0 / n_topics if n_topics > 0 else 0.0
    last_cnt = float(counts[-1]) if n else 0.0
    prev_cnt = float(counts[-2]) if n >= 2 else 0.0
    recent_max_rel = float(np.max(counts[-3:]) / w_mean) if n >= 3 and w_mean > 0 else 1.0
    feats.extend([is_core, quota, float(n_topics), topic_share, last_cnt, prev_cnt, recent_max_rel])

    # ---- Comparison features (13) -------------------------------------
    subj_counts = [np.mean(all_td[k]["counts"]) for k in all_td if all_td[k]["subject"] == subj]
    subj_avg = float(np.mean(subj_counts)) if subj_counts else w_mean
    relative_importance = w_mean / subj_avg if subj_avg > 0 else 1.0

    all_means = [np.mean(all_td[k]["counts"]) for k in all_td]
    global_avg = float(np.mean(all_means)) if all_means else w_mean
    global_relative = w_mean / global_avg if global_avg > 0 else 1.0

    hist_peak_rel = float(counts.max() / counts.mean()) if counts.mean() > 0 else 1.0
    years_active = float(n)
    first_year_seen = float(min(years))
    total_history = float(np.sum(counts))
    count_10yr = float(np.sum([c for y, c in zip(years, counts) if y >= target_year - 10]))
    count_5yr = float(np.sum([c for y, c in zip(years, counts) if y >= target_year - 5]))
    count_3yr = float(np.sum([c for y, c in zip(years, counts) if y >= target_year - 3]))
    recency_weighted_total = float(np.sum(
        [c * np.exp(-(target_year - y) / tau) for y, c in zip(years, counts)]))
    trend_ratio = float(np.mean(counts[-2:]) / np.mean(counts[:2])) if n >= 4 and np.mean(counts[:2]) > 0 else 1.0
    pred_prob_appearing = float(np.clip(appear_rate * np.exp(-years_since / 4.0), 0, 1))
    feats.extend([
        relative_importance, global_relative, hist_peak_rel,
        years_active, first_year_seen, total_history,
        count_10yr, count_5yr, count_3yr,
        recency_weighted_total, trend_ratio, pred_prob_appearing,
        float(np.mean(counts[-2:]) if n >= 2 else counts[-1])
    ])

    # Final length check
    if len(feats) != FEATURE_DIM:
        # pad or truncate – should not happen
        if len(feats) < FEATURE_DIM:
            feats += [0.0] * (FEATURE_DIM - len(feats))
        else:
            feats = feats[:FEATURE_DIM]
    return np.nan_to_num(np.array(feats, dtype=float), nan=0.0, posinf=10.0, neginf=-10.0)

# ----------------------------------------------------------------------
# 8.  Confidence calibrator (isotonic + blend)
# ----------------------------------------------------------------------
class Calibrator:
    def __init__(self):
        self._xs: List[float] = []
        self._ys: List[float] = []
        self._model = None
        self._ready = False

    def record(self, raw: float, accuracy: float):
        self._xs.append(float(np.clip(raw, 0, 1)))
        self._ys.append(float(np.clip(accuracy, 0, 1)))

    def fit(self):
        if len(self._xs) < 5 or not SKLEARN:
            return
        try:
            self._model = IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds="clip")
            self._model.fit(self._xs, self._ys)
            self._ready = True
        except Exception as e:
            print(f"   ⚠️  Calibrator fit failed: {e}")

    def calibrate(self, raw: float) -> float:
        rc = float(np.clip(raw, 0, 1))
        if not self._ready or self._model is None:
            return float(np.clip(rc * 0.75 + 0.10, 0.10, 0.85))
        cal = float(self._model.predict([rc])[0])
        blended = CONF_BLEND * rc + (1 - CONF_BLEND) * cal
        spread = (rc - 0.5) * 0.20
        return float(np.clip(blended + spread, 0.10, 0.85))

    @property
    def ece(self) -> float:
        if not self._xs:
            return 0.0
        xs, ys = np.array(self._xs), np.array(self._ys)
        ece = 0.0
        for i in range(10):
            lo, hi = i / 10, (i + 1) / 10
            mask = (xs >= lo) & (xs < hi)
            if mask.sum() > 0:
                ece += mask.sum() / len(xs) * abs(xs[mask].mean() - ys[mask].mean())
        return round(float(ece), 4)

# ----------------------------------------------------------------------
# 9.  Predictor (best of both)
# ----------------------------------------------------------------------
class BestPredictor:
    def __init__(self):
        self.scaler = RobustScaler() if SKLEARN else None
        self.models: Dict[str, Any] = {}
        self.stacker = None
        self.topic_data: dict = {}
        self.micro_data: dict = {}
        self.calibrator = Calibrator()
        self.train_metrics: dict = {}
        self.learned_tau: Dict[str, float] = {}      # per‑subject for topics (optional)
        self.micro_learned_tau: Dict[str, float] = {} # per‑subject for micro
        self.canonical_taxonomy: dict = {}            # loaded from canonical_taxonomy.json
        self.learned_kappa: float = DIRICHLET_KAPPA
        self.learned_delta: float = DIRICHLET_DELTA
        self._load_canonical_taxonomy()

    def _load_canonical_taxonomy(self):
        """Load canonical_taxonomy.json mapping 449 raw labels → 86 syllabus concepts."""
        tax_path = Path("canonical_taxonomy.json")
        if not tax_path.exists():
            # Try relative to script location
            tax_path = Path(__file__).parent / "canonical_taxonomy.json"
        if tax_path.exists():
            with open(tax_path, "r", encoding="utf-8") as f:
                self.canonical_taxonomy = json.load(f)
            n_concepts = len(set(
                c for d in self.canonical_taxonomy.values()
                for c in d["label_to_concept"].values()
            ))
            print(f"   ✓ Loaded canonical taxonomy: {sum(len(d['label_to_concept']) for d in self.canonical_taxonomy.values())} labels → {n_concepts} concepts")
        else:
            print("   ⚠️  canonical_taxonomy.json not found – falling back to raw-label mode")

    def _get_canonical_concept(self, subject: str, topic: str, micro: str) -> str:
        """Map a raw micro-topic label to its canonical syllabus concept."""
        pk = f"{subject}::{topic}"
        if pk in self.canonical_taxonomy:
            mapping = self.canonical_taxonomy[pk].get("label_to_concept", {})
            return mapping.get(micro, "OTHER")
        return "OTHER"

    # ------------------------------------------------------------------
    # 9a. Model zoo (same as Ultimate + CatBoost if available)
    # ------------------------------------------------------------------
    def _build_models(self):
        models = {}
        if XGBOOST:
            models["xgb"] = xgb.XGBRegressor(
                n_estimators=500, learning_rate=0.015, max_depth=6,
                min_child_weight=5, subsample=0.7, colsample_bytree=0.7,
                gamma=0.2, reg_alpha=0.5, reg_lambda=2.0,
                objective="count:poisson", random_state=42,
                tree_method="hist", verbosity=0)
        if LIGHTGBM:
            models["lgb"] = lgb.LGBMRegressor(
                n_estimators=500, learning_rate=0.015, num_leaves=31,
                min_child_samples=15, subsample=0.7, colsample_bytree=0.7,
                reg_alpha=0.5, reg_lambda=2.0,
                objective="poisson", random_state=42, verbose=-1)
        if SKLEARN:
            models["et"] = ExtraTreesRegressor(
                n_estimators=400, max_depth=10, min_samples_split=8,
                min_samples_leaf=5, max_features="sqrt", random_state=42, n_jobs=2)
            models["rf"] = RandomForestRegressor(
                n_estimators=350, max_depth=10, min_samples_split=8,
                min_samples_leaf=5, max_features="sqrt", random_state=42, n_jobs=2)
            models["hgb"] = HistGradientBoostingRegressor(
                max_iter=400, learning_rate=0.02, max_depth=8,
                min_samples_leaf=8, l2_regularization=2.0, random_state=42)
        # CatBoost optional – only if available
        try:
            import catboost as cb
            models["cb"] = cb.CatBoostRegressor(
                iterations=600, learning_rate=0.012, depth=6,
                loss_function="Poisson", random_seed=42, verbose=False)
        except ImportError:
            pass
        self.models = models
        print(f"   ✓ Built {len(models)} models: {list(models.keys())}")
        return list(models.items())

    # ------------------------------------------------------------------
    # 9b. Learn per‑subject τ (for topics) – grid search on walk‑forward
    # ------------------------------------------------------------------
    def learn_tau_per_subject(self, topic_data: dict, years_range: Optional[List[int]] = None):
        """Learn optimal τ per subject using recency-weighted walk-forward."""
        if years_range is None:
            years_range = list(range(2018, 2026))

        # Build nested structure: subject -> topic -> {year: count}
        subj_topics = defaultdict(lambda: defaultdict(dict))
        for k, d in topic_data.items():
            subj = d["subject"]
            topic = d["topic"]
            for y in d["years"]:
                subj_topics[subj][topic][y] = d["counts"][d["years"].index(y)]

        for subj in SECTION_DISTRIBUTION:
            st = subj_topics.get(subj, {})
            if not st:
                self.learned_tau[subj] = TOPIC_TAU
                continue
            best_tau, best_err = TOPIC_TAU, float("inf")
            for tau in TAU_GRID:
                weighted_num = 0.0
                weighted_den = 0.0
                for test_year in years_range:
                    yr_weight = float(np.exp(-(TARGET_YEAR_FOR_TAU - test_year) / TAU_RECENCY_SCALE))
                    target = SECTION_DISTRIBUTION.get(subj, 5)
                    preds, actuals = [], []
                    for topic, yc in st.items():
                        train_yc = {y: c for y, c in yc.items() if y < test_year}
                        if not train_yc:
                            continue
                        last_seen = max(train_yc.keys())
                        total = sum(train_yc.values())
                        recency = np.exp(-(test_year - last_seen) / tau)
                        preds.append(total * recency)
                        actuals.append(yc.get(test_year, 0))
                    if preds:
                        sp = sum(preds)
                        if sp > 0:
                            preds = [p / sp * target for p in preds]
                        for p, a in zip(preds, actuals):
                            if a > 0:
                                weighted_num += abs(p - a) * yr_weight
                                weighted_den += yr_weight
                if weighted_den > 0:
                    mae = weighted_num / weighted_den
                    if mae < best_err:
                        best_err, best_tau = mae, tau
            self.learned_tau[subj] = best_tau
        print(f"   ✓ Learned topic τ per subject: {dict(sorted(self.learned_tau.items()))}")

    # ------------------------------------------------------------------
    # 9c. Learn per‑subject τ for micro‑topics (similar grid)
    # ------------------------------------------------------------------
    def learn_micro_tau_per_subject(self, micro_data: dict, years_range: Optional[List[int]] = None):
        """Learn optimal κ (prior strength) and δ (recency discount) for Dirichlet micro model."""
        # Also keep legacy micro tau for compatibility
        for subj in SECTION_DISTRIBUTION:
            base_tau = self.learned_tau.get(subj, TOPIC_TAU)
            self.micro_learned_tau[subj] = min(base_tau * 1.3, 5.0)

        if not self.canonical_taxonomy:
            print(f"   ✓ Learned micro τ per subject (legacy): {dict(sorted(self.micro_learned_tau.items()))}")
            return

        # Grid search κ and δ on walk-forward canonical concept recall
        if years_range is None:
            years_range = list(range(2020, 2027))

        best_kappa, best_delta, best_score = DIRICHLET_KAPPA, DIRICHLET_DELTA, -1.0
        for kappa in KAPPA_GRID:
            for delta in DELTA_GRID:
                total_recall = 0.0
                n_years = 0
                for test_year in years_range:
                    # Build canonical concept counts from micro_data up to test_year
                    recall = self._dirichlet_recall_for_year(
                        micro_data, test_year, kappa, delta
                    )
                    if recall is not None:
                        total_recall += recall
                        n_years += 1
                if n_years > 0:
                    avg_recall = total_recall / n_years
                    if avg_recall > best_score:
                        best_score = avg_recall
                        best_kappa = kappa
                        best_delta = delta

        self.learned_kappa = best_kappa
        self.learned_delta = best_delta
        print(f"   ✓ Learned Dirichlet params: κ={best_kappa}, δ={best_delta} (canonical recall={best_score:.1f}%)")

    def _dirichlet_recall_for_year(self, micro_data, test_year, kappa, delta):
        """Compute canonical concept recall for one walk-forward year."""
        from collections import defaultdict as dd
        # Build per-topic canonical concept counts for training years
        # and actual canonical concepts for test year
        all_questions = []
        for mk, d in micro_data.items():
            for i, y in enumerate(d["years"]):
                if d["counts"][i] > 0:
                    all_questions.append({
                        "subject": d["subject"], "topic": d["topic"],
                        "micro": d["micro"], "year": y, "count": d["counts"][i]
                    })

        # Get actual canonical concepts in test year
        actual_concepts = set()
        for q in all_questions:
            if q["year"] == test_year and q["count"] > 0:
                concept = self._get_canonical_concept(q["subject"], q["topic"], q["micro"])
                pk = f"{q['subject']}::{q['topic']}"
                actual_concepts.add(f"{pk}::{concept}")

        if not actual_concepts:
            return None

        # Build Dirichlet predictions for each topic
        # Gather concept counts per topic per year
        concept_year_counts = dd(lambda: dd(float))  # {pk::concept: {year: count}}
        for q in all_questions:
            if q["year"] < test_year:
                concept = self._get_canonical_concept(q["subject"], q["topic"], q["micro"])
                pk = f"{q['subject']}::{q['topic']}"
                ck = f"{pk}::{concept}"
                concept_year_counts[ck][q["year"]] += q["count"]

        # For each topic, compute Dirichlet allocation
        predicted_concepts = set()
        topics_seen = set()
        for ck in concept_year_counts:
            parts = ck.rsplit("::", 1)
            topics_seen.add(parts[0])

        for pk in topics_seen:
            # Get all concepts under this topic from taxonomy
            if pk in self.canonical_taxonomy:
                all_concepts_here = list(set(self.canonical_taxonomy[pk]["label_to_concept"].values()))
            else:
                all_concepts_here = []
            all_concepts_here.append("OTHER")

            # Compute alpha for each concept
            K = len(all_concepts_here)
            for concept in all_concepts_here:
                ck = f"{pk}::{concept}"
                # Prior
                if concept == "OTHER":
                    q_k = OTHER_PRIOR_FRAC
                else:
                    q_k = (1.0 - OTHER_PRIOR_FRAC) / max(1, K - 1)
                alpha = kappa * q_k

                # Add discounted historical evidence
                if ck in concept_year_counts:
                    for yr, cnt in concept_year_counts[ck].items():
                        alpha += (delta ** (test_year - yr)) * cnt

                if alpha > kappa * q_k + 0.01:  # has some historical evidence
                    predicted_concepts.add(ck)

        # Also add all concepts from taxonomy for seen topics (Bayesian: non-zero prior)
        for pk in topics_seen:
            if pk in self.canonical_taxonomy:
                for concept in set(self.canonical_taxonomy[pk]["label_to_concept"].values()):
                    predicted_concepts.add(f"{pk}::{concept}")

        hits = len(actual_concepts & predicted_concepts)
        recall = hits / len(actual_concepts) * 100 if actual_concepts else 0.0
        return recall

    # ------------------------------------------------------------------
    # 9d. Training (stacking ensemble)
    # ------------------------------------------------------------------
    def train(self, questions: List[dict]) -> dict:
        print("\n🔧 Training Best v8.0 ensemble …")
        self.topic_data, self.micro_data = build_data(questions)
        print(f"   ✓ {len(self.topic_data)} topics | {len(self.micro_data)} micro-topics")

        # Learn per‑subject decay constants
        self.learn_tau_per_subject(self.topic_data)
        self.learn_micro_tau_per_subject(self.micro_data)

        # Build training set for topic model
        X_list, y_list, sample_years = [], [], []
        for k, d in self.topic_data.items():
            if len(d["years"]) < 4:
                continue
            for i in range(3, len(d["years"])):
                hist = {
                    "years": d["years"][:i],
                    "counts": d["counts"][:i],
                    "subject": d["subject"],
                    "topic": d["topic"]
                }
                feat = extract_features(hist, self.topic_data, d["years"][i], self.learned_tau)
                X_list.append(feat)
                y_list.append(d["counts"][i])
                sample_years.append(d["years"][i])

        if not X_list:
            print("   ❌ Insufficient training data")
            return {}

        X = np.array(X_list, dtype=float)
        y = np.array(y_list, dtype=float)
        wt = np.array([era_weight(yr) for yr in sample_years], dtype=float)

        print(f"   ✓ Training samples: {len(X)} | Features: {X.shape[1]}")
        if self.scaler:
            X = self.scaler.fit_transform(X)

        # Build base models
        estimators = self._build_models()
        if not estimators:
            print("   ⚠️  No ML models available – using fallback")
            return {}

        # Cross‑validation scores (optional)
        if SKLEARN:
            tscv = TimeSeriesSplit(n_splits=8)
            print("   📊 CV MAE per model:")
            for name, model in self.models.items():
                errs = []
                for tr, va in tscv.split(X):
                    try:
                        kw = {"sample_weight": wt[tr]} if name in ("xgb", "lgb", "cb") else {}
                        model.fit(X[tr], y[tr], **kw)
                        errs.append(mean_absolute_error(y[va], np.clip(model.predict(X[va]), 0, 25)))
                    except Exception as e:
                        print(f"      ⚠️  {name}: {e}")
                if errs:
                    print(f"      {name:6s}: {np.mean(errs):.4f}")

        # Stacking
        if SKLEARN and len(self.models) >= 2:
            print("   🧱 Stacking meta‑learner …")
            est_list = list(self.models.items())[:5]   # limit to 5 for speed
            self.stacker = StackingRegressor(
                estimators=est_list,
                final_estimator=BayesianRidge(),
                cv=5, n_jobs=2
            )
            oof = np.clip(cross_val_predict(self.stacker, X, y, cv=5, n_jobs=2), 0, 25)
            self.stacker.fit(X, y, sample_weight=wt)
            self.train_metrics = {
                "MAE": round(float(mean_absolute_error(y, oof)), 4),
                "RMSE": round(float(np.sqrt(mean_squared_error(y, oof))), 4),
                "R2": round(float(r2_score(y, oof)), 4),
            }
            print(f"   🎯 Stacker OOF: {self.train_metrics}")
        return self.train_metrics

    # ------------------------------------------------------------------
    # 9e. Raw confidence (fusion weighting)
    # ------------------------------------------------------------------
    def _raw_conf(self, d: dict, pred: float, std: float, target_year: int) -> float:
        n = len(d["years"])
        mu = float(np.mean(d["counts"]))
        cv = float(np.std(d["counts"])) / mu if mu > 0 else 1.0
        ls = max(d["years"])
        tau = self.learned_tau.get(d.get("subject", ""), TOPIC_TAU)
        rec = np.exp(-(target_year - ls) / tau)
        span = max(d["years"]) - min(d["years"]) + 1 if n > 1 else 1
        ar = n / span
        core = 0.9 if d["topic"] in CORE_TOPICS.get(d["subject"], []) else 0.5
        stab = 1.0 / (1 + cv)
        unc = 1.0 / (1 + std) if std > 0 else 0.8
        ok = 1.0 if 0.3 <= pred <= 10 else max(0.3, 1 - abs(pred - 5) / 10)
        data = min(1.0, n / 12)
        factors = [data, stab, rec, ar, core, unc, ok]
        weights = [0.5, 1.5, 2.2, 1.0, 1.3, 2.0, 0.9]
        conf = float(np.average(factors, weights=weights[:len(factors)]))
        return float(np.clip(conf, 0.10, 0.98))

    def _trend(self, d: dict) -> str:
        c = d["counts"]
        if len(c) < 3:
            return "Stable"
        recent = np.mean(c[-3:])
        older = np.mean(c[:-3]) if len(c) > 3 else np.mean(c)
        if older == 0:
            return "Emerging" if recent > 0 else "Stable"
        ch = (recent - older) / older * 100
        return "Rising" if ch > 30 else ("Declining" if ch < -30 else "Stable")

    # ------------------------------------------------------------------
    # 9f. Topic predictions (with learned τ and false‑positive suppression)
    # ------------------------------------------------------------------
    def predict_topics(self, target_year: int = 2027) -> List[dict]:
        print(f"\n🔮 Topic predictions for {target_year} …")
        raw = []

        for k, d in self.topic_data.items():
            if len(d["years"]) < MIN_APPEARANCES:
                continue
            if max(d["years"]) < MIN_LAST_SEEN:
                continue

            # Features
            feat = extract_features(d, self.topic_data, target_year, self.learned_tau)
            if self.scaler:
                feat_s = self.scaler.transform(feat.reshape(1, -1))
            else:
                feat_s = feat.reshape(1, -1)

            # Ensemble prediction
            ind_preds = []
            if self.stacker:
                base = float(self.stacker.predict(feat_s)[0])
                for m in self.models.values():
                    try:
                        ind_preds.append(float(m.predict(feat_s)[0]))
                    except:
                        pass
            elif self.models:
                for m in self.models.values():
                    try:
                        ind_preds.append(float(m.predict(feat_s)[0]))
                    except:
                        pass
                base = float(np.mean(ind_preds)) if ind_preds else float(np.average(
                    d["counts"], weights=[era_weight(y) for y in d["years"]]))
            else:
                base = float(np.average(d["counts"], weights=[era_weight(y) for y in d["years"]]))
                ind_preds = [base]

            pred = max(0.0, base)
            std = float(np.std(ind_preds)) if len(ind_preds) > 1 else 0.0

            # False-positive suppression with subject-specific decay
            ls = max(d["years"])
            ys = target_year - ls
            tau = self.learned_tau.get(d["subject"], TOPIC_TAU)
            ar = len(d["years"]) / max(1, max(d["years"]) - min(d["years"]) + 1)
            if ys > 5:
                pred *= float(np.exp(-ys / max(2.0, tau)))
            elif ys > 3 and ar < 0.25:
                pred *= float(np.exp(-ys / max(2.5, tau + 0.5)))

            # Prediction interval (bootstrap)
            if len(ind_preds) >= 2:
                ip = np.clip(ind_preds, 0, 25)
                cv_ = float(np.std(d["counts"]) / np.mean(d["counts"])) if np.mean(d["counts"]) > 0 else 1.0
                width_mult = 1.0 + min(cv_, 1.5) * 0.3
                p10 = float(np.percentile(ip, 10))
                p90 = float(np.percentile(ip, 90))
                half_width = max(p90 - p10, 0.1) / 2.0 * width_mult
                lower = max(0.0, pred - half_width)
                upper = pred + half_width
            else:
                lower = max(0.0, pred * 0.7)
                upper = pred * 1.3

            # Confidence
            raw_conf = self._raw_conf(d, pred, std, target_year)
            cal_conf = self.calibrator.calibrate(raw_conf)

            raw.append({
                "subject": d["subject"],
                "topic": d["topic"],
                "predicted_count": round(pred, 3),
                "confidence": round(cal_conf * 100, 1),
                "raw_confidence": round(raw_conf * 100, 1),
                "uncertainty": round(std, 3),
                "lower_bound": round(lower, 3),
                "upper_bound": round(upper, 3),
                "trend": self._trend(d),
                "hist_avg": round(float(np.mean(d["counts"])), 2),
                "recent_avg": round(float(np.mean(d["counts"][-3:])) if len(d["counts"]) >= 3 else float(np.mean(d["counts"])), 2),
                "last_seen": int(ls),
                "appearances": len(d["years"]),
                "is_core": "✓" if d["topic"] in CORE_TOPICS.get(d["subject"], []) else "",
            })

        print(f"   ✓ {len(raw)} raw topic predictions")
        return self._normalize_topics(raw)

    # ------------------------------------------------------------------
    # 9g. Normalise topic predictions to GATE quotas
    # ------------------------------------------------------------------
    def _normalize_topics(self, preds: List[dict]) -> List[dict]:
        kept = [p for p in preds if p["confidence"] >= MIN_CONF_THRESHOLD * 100]
        raw_map = {f"{p['subject']}::{p['topic']}": p["predicted_count"] for p in kept}

        by_subj = defaultdict(list)
        for p in kept:
            by_subj[p["subject"]].append(p)

        result = []
        for subj, quota in SECTION_DISTRIBUTION.items():
            topics = by_subj.get(subj, [])
            if not topics:
                core = CORE_TOPICS.get(subj, [subj])[:max(1, quota)]
                for t in core[:quota]:
                    result.append({
                        "subject": subj, "topic": t,
                        "predicted_count": round(quota / len(core[:quota]), 2),
                        "confidence": 40.0, "raw_confidence": 40.0,
                        "trend": "Core", "is_core": "✓"
                    })
                continue

            # Weighted distribution
            for p in topics:
                p["_w"] = p["predicted_count"] * (p["confidence"] / 100) ** 0.8
            tw = sum(p["_w"] for p in topics) or 1.0

            for p in topics:
                norm_pred = (p["_w"] / tw) * quota
                raw_pred = raw_map.get(f"{p['subject']}::{p['topic']}", norm_pred)
                p["predicted_count"] = NORM_BLEND * raw_pred + (1 - NORM_BLEND) * norm_pred
                del p["_w"]

            # Rescale to exact quota
            cs = sum(p["predicted_count"] for p in topics)
            if cs > 0:
                sf = quota / cs
                for p in topics:
                    p["predicted_count"] = round(p["predicted_count"] * sf, 3)
                    for field in ("lower_bound", "upper_bound"):
                        if field in p:
                            p[field] = round(p[field] * sf, 3)
            result.extend(topics)

        # Global rescale to 65
        total = sum(p["predicted_count"] for p in result)
        if total > 0 and abs(total - TOTAL_GATE_QUESTIONS) > 0.1:
            sf = TOTAL_GATE_QUESTIONS / total
            for p in result:
                p["predicted_count"] = round(p["predicted_count"] * sf, 3)

        # Relative confidence re‑anchoring (v5 technique)
        by_s = defaultdict(list)
        for p in result:
            by_s[p["subject"]].append(p)
        for grp in by_s.values():
            tot_s = sum(p["predicted_count"] for p in grp)
            n = len(grp)
            eq = tot_s / n if n else 1.0
            for p in grp:
                rc = p.get("raw_confidence", p["confidence"]) / 100
                rel = p["predicted_count"] / eq if eq > 0 else 1.0
                rel_conf = float(np.clip(0.35 + (rel - 1.0) * 0.15, 0.12, 0.84))
                p["confidence"] = round(float(np.clip(0.60 * rc + 0.40 * rel_conf, 0.10, 0.84)) * 100, 1)

        result.sort(key=lambda x: (x["confidence"], x["predicted_count"]), reverse=True)
        print(f"   ✓ {len(result)} topics normalised → {sum(p['predicted_count'] for p in result):.1f} questions")
        return result

    # ------------------------------------------------------------------
    # 9h. Micro‑topic predictions (Canonical Dirichlet Model)
    # ------------------------------------------------------------------
    def predict_micro(self, topic_preds: List[dict], target_year: int) -> List[dict]:
        print(f"\n🔬 Micro‑topic predictions for {target_year} (Canonical Dirichlet) …")
        parent_quota = {f"{p['subject']}::{p['topic']}": p["predicted_count"] for p in topic_preds}

        if not self.canonical_taxonomy:
            return self._predict_micro_legacy(topic_preds, target_year)

        kappa = self.learned_kappa
        delta = self.learned_delta

        # Step 1: Build per-concept per-year count history from micro_data
        concept_year_counts = defaultdict(lambda: defaultdict(float))  # {pk::concept: {year: count}}
        concept_raw_labels = defaultdict(lambda: defaultdict(list))    # {pk::concept: {year: [labels]}}
        for mk, d in self.micro_data.items():
            pk = f"{d['subject']}::{d['topic']}"
            concept = self._get_canonical_concept(d["subject"], d["topic"], d["micro"])
            ck = f"{pk}::{concept}"
            for i, y in enumerate(d["years"]):
                if y < target_year and d["counts"][i] > 0:
                    concept_year_counts[ck][y] += d["counts"][i]
                    concept_raw_labels[ck][y].append(d["micro"])

        result = []
        concept_count = 0
        for pk, quota in parent_quota.items():
            if quota <= 0:
                continue

            # Get all canonical concepts for this topic
            if pk in self.canonical_taxonomy:
                all_concepts = list(set(self.canonical_taxonomy[pk]["label_to_concept"].values()))
            else:
                all_concepts = []
            all_concepts_with_other = all_concepts + ["OTHER"]
            K = len(all_concepts_with_other)

            # Step 2: Compute Dirichlet posterior α for each concept
            alphas = {}
            for concept in all_concepts_with_other:
                ck = f"{pk}::{concept}"
                # Prior: uniform over known concepts, OTHER gets its own fraction
                if concept == "OTHER":
                    q_k = OTHER_PRIOR_FRAC
                else:
                    q_k = (1.0 - OTHER_PRIOR_FRAC) / max(1, K - 1)
                alpha = kappa * q_k

                # Discounted historical evidence: Σ δ^(t-r) Y_{r,k}
                if ck in concept_year_counts:
                    for yr, cnt in concept_year_counts[ck].items():
                        alpha += (delta ** (target_year - yr)) * cnt

                alphas[concept] = alpha

            # Step 3: Expected allocation θ_k = α_k / Σα_j, then N_k = θ_k × quota
            total_alpha = sum(alphas.values())
            for concept in all_concepts_with_other:
                theta = alphas[concept] / total_alpha if total_alpha > 0 else 1.0 / K
                pred_cnt = round(theta * quota, 3)

                if pred_cnt < MICRO_PRED_TH:
                    continue

                # Compute confidence from alpha strength
                evidence = alphas[concept] - kappa * (OTHER_PRIOR_FRAC if concept == "OTHER" else (1.0 - OTHER_PRIOR_FRAC) / max(1, K - 1))
                data_factor = min(1.0, evidence / 5.0)
                conf = round(float(np.clip(0.3 + 0.5 * data_factor + 0.2 * theta, 0.15, 0.85)) * 100, 1)

                # Determine trend from recent history
                ck = f"{pk}::{concept}"
                recent_years = sorted([y for y in concept_year_counts.get(ck, {}).keys() if y >= target_year - 5])
                if len(recent_years) >= 2:
                    recent_counts = [concept_year_counts[ck][y] for y in recent_years]
                    trend = "↑" if recent_counts[-1] > np.mean(recent_counts[:-1]) else "↓" if recent_counts[-1] < np.mean(recent_counts[:-1]) * 0.5 else "→"
                elif len(recent_years) == 1:
                    trend = "→"
                else:
                    trend = "↓" if concept != "OTHER" else "→"

                # Get representative raw labels for display
                all_raw = []
                for yr_labels in concept_raw_labels.get(ck, {}).values():
                    all_raw.extend(yr_labels)
                top_raw = Counter(all_raw).most_common(3)
                raw_label_str = ", ".join(l for l, _ in top_raw) if top_raw else concept

                # Tier assignment
                if pred_cnt >= quota * 0.25:
                    tier = "High Priority"
                elif pred_cnt >= MICRO_PRED_TH * 2:
                    tier = "Core Coverage"
                else:
                    tier = "Novelty Protection" if concept == "OTHER" else "Core Coverage"

                parts = pk.split("::")
                result.append({
                    "subject": parts[0],
                    "topic": parts[1],
                    "micro_topic": concept,
                    "canonical_concept": concept,
                    "raw_labels": raw_label_str,
                    "predicted_count": pred_cnt,
                    "confidence": conf,
                    "trend": trend,
                    "alpha": round(alphas[concept], 3),
                    "theta": round(theta, 4),
                    "tier": tier,
                })
                concept_count += 1

        result.sort(key=lambda x: (x["confidence"], x["predicted_count"]), reverse=True)
        n_high = sum(1 for r in result if r["tier"] == "High Priority")
        n_core = sum(1 for r in result if r["tier"] == "Core Coverage")
        n_novel = sum(1 for r in result if r["tier"] == "Novelty Protection")
        print(f"   ✓ {len(result)} canonical concept predictions ({concept_count} concepts)")
        print(f"   ✓ Tiers: {n_high} High Priority | {n_core} Core Coverage | {n_novel} Novelty Protection")
        print(f"   ✓ Dirichlet params: κ={kappa}, δ={delta}")
        return result

    def _predict_micro_legacy(self, topic_preds: List[dict], target_year: int) -> List[dict]:
        """Legacy EMA-based micro prediction (fallback when taxonomy unavailable)."""
        parent_quota = {f"{p['subject']}::{p['topic']}": p["predicted_count"] for p in topic_preds}
        parent_totals = defaultdict(float)
        for d in self.micro_data.values():
            pk = f"{d['subject']}::{d['topic']}"
            parent_totals[pk] += sum(d["counts"])

        by_parent = defaultdict(list)
        for d in self.micro_data.values():
            non_zero_years = [y for y, c in zip(d["years"], d["counts"]) if c > 0]
            if len(non_zero_years) < 2:
                continue
            if max(non_zero_years) < 2016:
                continue

            pk = f"{d['subject']}::{d['topic']}"
            ls = max(non_zero_years)
            ys = target_year - ls
            total = sum(d["counts"])
            n = len(non_zero_years)

            tau = self.micro_learned_tau.get(d["subject"], MICRO_TAU)
            score = ema(d["counts"], MICRO_EMA_ALPHA) * np.exp(-ys / tau)

            span = max(d["years"]) - min(d["years"]) + 1 if len(d["years"]) > 1 else 1
            consistency = n / span
            data_factor = min(1.0, n / 8)
            recency_factor = np.exp(-ys / 2.5)
            wtf = total / parent_totals[pk] if parent_totals[pk] > 0 else 0.0
            conf_raw = 0.28 * data_factor + 0.28 * recency_factor + 0.22 * consistency + 0.22 * wtf
            conf = round(float(np.clip(conf_raw, 0.15, 0.85)) * 100, 1)

            by_parent[pk].append({
                "subject": d["subject"], "topic": d["topic"],
                "micro_topic": d["micro"], "score": score, "confidence": conf,
                "trend": self._trend(d),
            })

        result = []
        for pk, cands in by_parent.items():
            quota = parent_quota.get(pk, 0)
            if not cands or quota <= 0:
                continue
            total_score = sum(c["score"] for c in cands)
            for c in cands:
                pred_cnt = round((c["score"] / total_score) * quota, 3) if total_score > 0 else 0.0
                if pred_cnt < MICRO_PRED_TH:
                    continue
                result.append({
                    "subject": c["subject"], "topic": c["topic"],
                    "micro_topic": c["micro_topic"],
                    "predicted_count": pred_cnt, "confidence": c["confidence"],
                    "trend": c["trend"],
                })
        result.sort(key=lambda x: (x["confidence"], x["predicted_count"]), reverse=True)
        print(f"   ✓ {len(result)} micro‑topic predictions (legacy EMA mode)")
        return result



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

    def predict_micro_new(self, target_year: int, max_new: int = 20) -> List[dict]:
        '''Predict unseen "New MT" micro-topics using a 3-signal architecture with syllabus exhaustion + decay.'''
        print(f"\n✨ Predicting New MT candidates for {target_year} …")

        import pathlib; syllabus_path = pathlib.Path("gate_syllabus.json")
        if not syllabus_path.exists():
            print("   ⚠️  gate_syllabus.json not found. Cannot predict new MTs.")
            return []

        with open(syllabus_path, "r", encoding="utf-8") as f:
            syllabus = json.load(f)

        # Determine first appearance year of each micro topic (< target_year)
        first_seen = {}
        for mk, d in self.micro_data.items():
            valid_years = [y for y, c in zip(d["years"], d["counts"]) if y < target_year and c > 0]
            if valid_years:
                first_seen[mk] = min(valid_years)

        topic_new_mt_count = defaultdict(int)
        subj_new_mt_count = defaultdict(int)
        topic_appearances = defaultdict(set)
        topic_last_seen = {}

        for k, d in self.topic_data.items():
            pk = f"{d['subject']}::{d['topic']}"
            valid_years = [y for y, c in zip(d["years"], d["counts"]) if y < target_year and c > 0]
            if valid_years:
                for y in valid_years:
                    topic_appearances[pk].add(y)
                topic_last_seen[pk] = max(valid_years)

        for mk, yr in first_seen.items():
            if yr >= 2011:
                parts = mk.split("::")
                subj, topic = parts[0], parts[1]
                pk = f"{subj}::{topic}"
                topic_new_mt_count[pk] += 1
                subj_new_mt_count[subj] += 1

        subj_total_qs = defaultdict(float)
        for mk, d in self.micro_data.items():
            parts = mk.split("::")
            subj = parts[0]
            count = sum(c for y, c in zip(d["years"], d["counts"]) if y >= 2011 and y < target_year)
            subj_total_qs[subj] += count

        topic_rate = {}
        for pk in topic_appearances:
            apps = len(topic_appearances[pk])
            topic_rate[pk] = topic_new_mt_count[pk] / apps if apps > 0 else 0

        subj_rate = {}
        for s in SECTION_DISTRIBUTION:
            if subj_total_qs[s] > 0:
                subj_rate[s] = subj_new_mt_count[s] / subj_total_qs[s]
            else:
                subj_rate[s] = 0

        max_t_rate = max(topic_rate.values()) if topic_rate else 1.0
        if max_t_rate == 0: max_t_rate = 1.0
        for pk in topic_rate:
            topic_rate[pk] /= max_t_rate

        seen_labels_normalized = set()
        for mk in first_seen.keys():
            parts = mk.split("::")
            if len(parts) >= 3:
                seen_labels_normalized.add(f"{parts[0]}::{parts[1]}::{norm_topic(parts[2]).lower()}")

        # PRE-COMPUTE Syllabus exhaustion per topic
        # Exhaustion Penalty = unseen / total_syllabus
        topic_exhaustion = {}
        for subj, topics in syllabus.items():
            for topic, mt_list in topics.items():
                pk = f"{subj}::{topic}"
                total_syl = len(mt_list)
                unseen = 0
                for mt in mt_list:
                    if f"{subj}::{topic}::{norm_topic(mt).lower()}" not in seen_labels_normalized:
                        unseen += 1
                val = (unseen / total_syl) if total_syl > 0 else 0.0
                topic_exhaustion[pk] = val

        candidates = []
        for subj, topics in syllabus.items():
            for topic, mt_list in topics.items():
                pk = f"{subj}::{topic}"
                exhaust = topic_exhaustion.get(pk, 0.0)
                
                for mt in mt_list:
                    norm_mt = norm_topic(mt).lower()
                    if f"{subj}::{topic}::{norm_mt}" not in seen_labels_normalized:
                        s1 = topic_rate.get(pk, 0.0)
                        s2 = subj_rate.get(subj, 0.0)

                        last_yr = topic_last_seen.get(pk, -1)
                        if last_yr > 0:
                            gap = target_year - last_yr
                            if gap == 1:
                                s3 = 1.0
                            elif gap in [2, 3]:
                                s3 = 0.5
                            else:
                                s3 = 0.3
                        else:
                            s3 = 0.1

                        base_score = (0.45 * s1 + 0.30 * s2 + 0.25 * s3) * exhaust

                        candidates.append({
                            "subject": subj,
                            "topic": topic,
                            "micro_topic": mt,
                            "canonical_concept": mt,
                            "raw_labels": f"{mt} [NEW]",
                            "predicted_count": 0.5,
                            "confidence": round((0.4 + base_score * 0.4) * 100, 1),
                            "trend": "New MT",
                            "base_score": base_score,
                            "score": base_score,
                            "tier": "Discovery",
                            "alpha": 0.0,
                            "theta": 0.0
                        })

        final_selected = []
        topic_picks = defaultdict(int)

        while len(final_selected) < max_new and candidates:
            # Re-decay
            for c in candidates:
                pk = f"{c['subject']}::{c['topic']}"
                c["score"] = c["base_score"] * (0.3 ** topic_picks[pk])
            
            candidates.sort(key=lambda x: x["score"], reverse=True)
            best = candidates.pop(0)

            if best["score"] >= 0.10:
                final_selected.append(best)
                topic_picks[f"{best['subject']}::{best['topic']}"] += 1
            else:
                break
                
        print(f"   ✓ Generated candidates, selected Top {len(final_selected)} New MTs (Decay applied)")
        return final_selected

# ----------------------------------------------------------------------
# 10.  Validator (walk‑forward with full metrics)
# ----------------------------------------------------------------------
class Validator:
    def __init__(self, predictor: BestPredictor, questions: List[dict]):
        self.pred = predictor
        self.questions = questions
        self.results: List[dict] = []

    def _snapshot_predict(self, train_q: List[dict], test_year: int):
        """Fast weighted‑average snapshot for walk‑forward (no retraining)."""
        td, md = build_data(train_q)
        raw = []
        for d in td.values():
            if len(d["years"]) < 2:
                continue
            w = [era_weight(y) for y in d["years"]]
            base = float(np.average(d["counts"], weights=w))
            ls = max(d["years"])
            ys = test_year - ls
            ar = len(d["years"]) / max(1, max(d["years"]) - min(d["years"]) + 1)
            if ys > 5:
                base *= np.exp(-ys / 4.0)
            elif ys > 3 and ar < 0.25:
                base *= np.exp(-ys / 5.0)
            rc = self.pred._raw_conf(d, base, 0, test_year)
            conf = self.pred.calibrator.calibrate(rc)
            raw.append({
                "subject": d["subject"], "topic": d["topic"],
                "predicted_count": max(0.0, base),
                "confidence": round(conf * 100, 1),
                "raw_confidence": round(rc * 100, 1),
                "trend": self.pred._trend(d)
            })
        return self.pred._normalize_topics(raw), td, md

    def run(self, test_years: Optional[List[int]] = None):
        if test_years is None:
            test_years = [2026, 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018]
        print("\n📊 Walk‑Forward Validation (3 levels) …")

        for ty in sorted(test_years):
            train_q = [q for q in self.questions if q["year"] < ty]
            test_q = [q for q in self.questions if q["year"] == ty]
            if len(train_q) < 100 or not test_q:
                print(f"   ⚠️  {ty}: insufficient data")
                continue

            np_ = MULTI_PAPER_YEARS.get(ty, 1)

            # Actual distributions
            act_subj = defaultdict(float)
            act_topic = defaultdict(float)
            act_micro = defaultdict(float)   # raw micro-topic labels (spelling-fixed)
            act_canon = defaultdict(float)   # canonical concepts
            for q in test_q:
                s, t, m = q["subject"], q["topic"], q["micro"]
                act_subj[s] += 1 / np_
                act_topic[f"{s}::{t}"] += 1 / np_
                act_micro[f"{s}::{t}::{m}"] += 1 / np_
                concept = self.pred._get_canonical_concept(s, t, m)
                act_canon[f"{s}::{t}::{concept}"] += 1 / np_

            # Predictions (snapshot)
            buf = io.StringIO()
            sys.stdout = buf
            try:
                norm_preds, td_snap, md_snap = self._snapshot_predict(train_q, ty)
            finally:
                sys.stdout = sys.__stdout__

            pred_subj = defaultdict(float)
            pred_topic = defaultdict(float)
            for p in norm_preds:
                pred_subj[p["subject"]] += p["predicted_count"]
                pred_topic[f"{p['subject']}::{p['topic']}"] += p["predicted_count"]

            # Feed calibration data
            for p in norm_preds:
                s = p["subject"]
                act = act_subj.get(s, 0)
                err = abs(pred_subj[s] - act)
                acc = 1.0 - min(1.0, err / max(1, act))
                self.pred.calibrator.record(p.get("raw_confidence", p["confidence"]) / 100, acc)

            # Micro predictions (snapshot)
            orig_micro = self.pred.micro_data
            self.pred.micro_data = md_snap
            buf2 = io.StringIO()
            sys.stdout = buf2
            try:
                micro_preds = self.pred.predict_micro(norm_preds, ty)
            finally:
                sys.stdout = sys.__stdout__
            self.pred.micro_data = orig_micro

            # Combine Old (250) + New (40) MTs
            # First, fetch New MT predictions
            buf3 = io.StringIO()
            sys.stdout = buf3
            try:
                micro_preds_new = self.pred.predict_micro_new(ty)
            finally:
                sys.stdout = sys.__stdout__

            micro_preds = micro_preds[:250] + micro_preds_new

            # Build micro-topic predictions: EXPAND concepts back to raw labels
            # This fixes the M_Hit measurement bug: the model predicts concepts
            # ("Minimum Spanning Trees") but M_Hit compares raw labels ("Kruskal's Algorithm").
            # We reverse-map each concept → all known raw labels for that concept,
            # distributing predicted_count by historical frequency within the concept.
            pred_micro = defaultdict(float)
            pred_canon = defaultdict(float)

            # Build reverse map: concept → {raw_label: historical_count} from training data
            concept_to_raw_counts = defaultdict(lambda: defaultdict(float))
            for q in train_q:
                s, t, m = q["subject"], q["topic"], q["micro"]
                concept = self.pred._get_canonical_concept(s, t, m)
                pk = f"{s}::{t}"
                ck = f"{pk}::{concept}"
                concept_to_raw_counts[ck][f"{pk}::{m}"] += q["count_inc"]

            for m in micro_preds:
                concept = m.get("canonical_concept", m["micro_topic"])
                pk = f"{m['subject']}::{m['topic']}"
                ck = f"{pk}::{concept}"
                pred_canon[ck] += m["predicted_count"]

                # Expand concept → raw labels proportionally
                raw_counts = concept_to_raw_counts.get(ck, {})
                if raw_counts:
                    total_raw = sum(raw_counts.values())
                    for raw_key, cnt in raw_counts.items():
                        frac = cnt / total_raw
                        pred_micro[raw_key] += m["predicted_count"] * frac
                else:
                    # No historical raw labels → use concept name as fallback
                    pred_micro[ck] += m["predicted_count"]

            # ---- Subject metrics ----
            subj_mae = float(np.mean([abs(pred_subj.get(s, 0) - act_subj.get(s, 0))
                                      for s in SECTION_DISTRIBUTION]))
            subj_mape_vals = [abs(pred_subj.get(s, 0) - act_subj.get(s, 0)) / act_subj[s]
                              for s in SECTION_DISTRIBUTION if act_subj.get(s, 0) > 0]
            subj_mape = float(np.mean(subj_mape_vals) * 100) if subj_mape_vals else 0.0
            subj_hit = float(sum(1 for s in SECTION_DISTRIBUTION
                                 if act_subj.get(s, 0) > 0 and pred_subj.get(s, 0) >= 0.5)
                             / max(1, sum(1 for s in SECTION_DISTRIBUTION if act_subj.get(s, 0) > 0)) * 100)

            # ---- Topic metrics ----
            def compute_level(pred_d, act_d, thresh):
                all_k = sorted(set(list(pred_d) + list(act_d)))
                pv = np.array([pred_d.get(k, 0) for k in all_k])
                av = np.array([act_d.get(k, 0) for k in all_k])
                mae = float(np.mean(np.abs(pv - av)))
                nz = av > 0
                mape = float(np.mean(np.abs((av[nz] - pv[nz]) / av[nz])) * 100) if nz.any() else 0.0
                hits = sum(1 for k in act_d if act_d[k] > 0 and pred_d.get(k, 0) >= thresh)
                n_act = sum(1 for k in act_d if act_d[k] > 0)
                hit_r = hits / n_act * 100 if n_act else 0.0
                ranked = sorted(all_k, key=lambda k: -pred_d.get(k, 0))
                act_set = {k for k in act_d if act_d[k] > 0}
                p10 = len(set(ranked[:10]) & act_set) / 10 * 100 if len(ranked) >= 10 else 0.0
                p20 = len(set(ranked[:20]) & act_set) / 20 * 100 if len(ranked) >= 20 else 0.0
                r20 = len(set(ranked[:20]) & act_set) / len(act_set) * 100 if act_set else 0.0

                # Question Coverage
                q_covered = sum(act_d[k] for k in act_d if pred_d.get(k, 0) >= thresh)
                total_q = sum(act_d.values())
                cov_pct = (q_covered / total_q * 100) if total_q > 0 else 0.0

                return {"mae": round(mae, 3), "mape": round(mape, 1),
                        "hit": round(hit_r, 1), "p10": round(p10, 1),
                        "p20": round(p20, 1), "r20": round(r20, 1),
                        "cov": round(cov_pct, 1)}

            t_met = compute_level(pred_topic, act_topic, TOPIC_HIT_TH)
            c_met = compute_level(dict(pred_canon), act_canon, MICRO_PRED_TH)
            m_met = compute_level(pred_micro, act_micro, MICRO_PRED_TH)

            row = {
                "year": ty, "n_papers": np_,
                "subj_mae": round(subj_mae, 3), "subj_mape": round(subj_mape, 1), "subj_hit": round(subj_hit, 1),
                "topic_mae": t_met["mae"], "topic_mape": t_met["mape"], "topic_hit": t_met["hit"],
                "topic_p10": t_met["p10"], "topic_p20": t_met["p20"], "topic_r20": t_met["r20"], "topic_cov": t_met["cov"],
                "canon_mae": c_met["mae"], "canon_mape": c_met["mape"], "canon_hit": c_met["hit"], "canon_cov": c_met["cov"],
                "micro_mae": m_met["mae"], "micro_mape": m_met["mape"], "micro_hit": m_met["hit"],
                "micro_p10": m_met["p10"], "micro_p20": m_met["p20"], "micro_r20": m_met["r20"], "micro_cov": m_met["cov"],
            }
            self.results.append(row)
            print(f"   {ty} ({np_}p)  "
                  f"S_MAE={subj_mae:.2f}  "
                  f"T_Hit={t_met['hit']:.0f}%  T_Cov={t_met['cov']:.0f}%  "
                  f"C_Hit={c_met['hit']:.0f}%  C_Cov={c_met['cov']:.0f}%  "
                  f"M_Hit={m_met['hit']:.0f}%  M_Cov={m_met['cov']:.0f}%")

        self.pred.calibrator.fit()
        print(f"\n   Calibration ECE: {self.pred.calibrator.ece}")
        return self.results

    def report(self):
        if not self.results:
            return
        r = self.results
        avg = lambda k: round(float(np.mean([x.get(k, 0) for x in r])), 2)

        print("\n" + "=" * 80)
        print("📋 VALIDATION REPORT — GATE 2027 BEST v8.0")
        print("=" * 80)
        print(f"\n  {len(r)}‑year walk‑forward (years: {[x['year'] for x in r]})")
        print(f"\n  ── SUBJECT LEVEL ───────────────────────────────────────────────")
        print(f"     MAE={avg('subj_mae')}  MAPE={avg('subj_mape')}%  HitRate={avg('subj_hit')}%")
        print(f"\n  ── TOPIC LEVEL ─────────────────────────────────────────────────")
        print(f"     MAE={avg('topic_mae')}  MAPE={avg('topic_mape')}%  "
              f"HitRate={avg('topic_hit')}%  Cov={avg('topic_cov')}%  P@10={avg('topic_p10')}%")
        print(f"\n  ── CONCEPT LEVEL (86 syllabus concepts) ───────────────────────")
        print(f"     MAE={avg('canon_mae')}  MAPE={avg('canon_mape')}%  "
              f"HitRate={avg('canon_hit')}%  Cov={avg('canon_cov')}%")
        print(f"\n  ── MICRO‑TOPIC LEVEL (442 fine-grained labels) ────────────────")
        print(f"     MAE={avg('micro_mae')}  MAPE={avg('micro_mape')}%  "
              f"HitRate={avg('micro_hit')}%  Cov={avg('micro_cov')}%  P@10={avg('micro_p10')}%")
        print(f"\n  ── PER‑YEAR ──────────────────────────────────────────────────────────────────────")
        print(f"  {'Year':>4}  {'S_MAE':>6}  {'T_Hit':>6}  {'T_Cov':>6}  "
              f"{'C_Hit':>6}  {'C_Cov':>6}  {'M_Hit':>6}  {'M_Cov':>6}")
        print("  " + "─" * 80)
        for row in sorted(r, key=lambda x: x["year"]):
            print(f"  {row['year']:>4}  {row['subj_mae']:>6.3f}  "
                  f"{row['topic_hit']:>5.1f}%  {row['topic_cov']:>5.1f}%  "
                  f"{row.get('canon_hit',0):>5.1f}%  {row.get('canon_cov',0):>5.1f}%  "
                  f"{row['micro_hit']:>5.1f}%  {row['micro_cov']:>5.1f}%")
        print(f"\n  Calibration ECE: {self.pred.calibrator.ece}")
        print("=" * 80)

# ----------------------------------------------------------------------
# 11.  Main
# ----------------------------------------------------------------------
def main():
    print("=" * 80)
    print("🎯  GATE 2027 FUSION PREDICTION SYSTEM  v9.0")
    print("    Elite stability + Ultimate tau learning + Best micro precision filter")
    print("=" * 80)
    print(f"📅  {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"📊  {TOTAL_GATE_QUESTIONS} questions | {len(SECTION_DISTRIBUTION)} subjects | {FEATURE_DIM} features")
    print("🤖  XGBoost + LightGBM + ExtraTrees + RF + HistGB + CatBoost (optional) → Stacking")
    print("🔬  Micro: EMA + per‑subject τ + precision filter")
    print("=" * 80)

    data_path = "Q.json"
    if not Path(data_path).exists():
        data_path = "/mnt/user-data/uploads/Q.json"

    questions = load_data(data_path, verbose=True)
    if len(questions) < 100:
        print("❌ Insufficient data")
        return

    predictor = BestPredictor()
    predictor.train(questions)

    validator = Validator(predictor, questions)
    validator.run([2026, 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018])
    validator.report()

    # Retrain on full data for final 2027 prediction
    print("\n" + "=" * 80)
    print("🔄 Retraining on full 2011‑2026 data for 2027 predictions …")
    print("=" * 80)
    final = BestPredictor()
    final.calibrator = predictor.calibrator   # reuse fitted calibrator
    final.train(questions)

    predictions = final.predict_topics(2027)
    concept_preds = final.predict_micro(predictions, 2027)
    
    # 7b. ML Ranked Raw Micro Topics (Strictly Top 250 Old)
    micro_predictions_old = final.expand_and_rank_micro_topics(concept_preds, 2027)
    
    # 8. New MT logic with Decay, capping at max 20
    micro_predictions_new = final.predict_micro_new(2027, max_new=20)

    micro_predictions = micro_predictions_old[:250] + micro_predictions_new

    # Display
    print("\n" + "=" * 80)
    print("✅  GATE 2027 PREDICTIONS")
    print("=" * 80)
    subj_tot = defaultdict(float)
    for p in predictions:
        subj_tot[p["subject"]] += p["predicted_count"]
    print(f"\n{'Subject':<32} {'Predicted':>10} {'Target':>8} {'Diff':>7}")
    print("─" * 60)
    for s in SECTION_DISTRIBUTION:
        pr = subj_tot.get(s, 0)
        tg = SECTION_DISTRIBUTION[s]
        d = pr - tg
        st = "✅" if abs(d) <= 1 else "⚠️"
        print(f"{st} {s[:30]:30s} {pr:>8.1f}  {tg:>7d}  {d:>+6.1f}")
    print(f"\n   Total: {sum(p['predicted_count'] for p in predictions):.1f}")

    print(f"\n🏆 Top 20 Topic Predictions:")
    for i, p in enumerate(predictions[:20], 1):
        bar = "█" * int(p["confidence"] / 10) + "░" * (10 - int(p["confidence"] / 10))
        print(f"  {i:2}. {p['subject'][:18]:18s} | {p['topic'][:28]:28s} "
              f"→ {p['predicted_count']:5.2f}q | {bar} {p['confidence']:.0f}%")

    print(f"\n🔬 Top 25 Micro‑Topic Predictions:")
    for i, m in enumerate(micro_predictions[:25], 1):
        bar = "█" * int(m["confidence"] / 10) + "░" * (10 - int(m["confidence"] / 10))
        print(f"  {i:2}. {m['topic'][:20]:20s} → {m['micro_topic'][:30]:30s} "
              f"{m['predicted_count']:5.3f}q | {bar} {m['confidence']:.0f}%")

    output = {
        "meta": {
            "version": "9.0 Fusion",
            "generated_at": datetime.now().isoformat(),
            "knobs": get_knobs(),
            "ece": predictor.calibrator.ece,
            "train_metrics": predictor.train_metrics,
            "walk_forward": validator.results,
            "learned_tau": predictor.learned_tau,
            "micro_learned_tau": predictor.micro_learned_tau,
        },
        "predictions": predictions,
        "micro_predictions": micro_predictions,
    }
    out_path = Path("gate2027_fusion_v9.json")
    out_path.write_text(json.dumps(output, indent=2, default=str), encoding="utf-8")
    print(f"\n💾 Saved: {out_path}")
    print(f"   {len(predictions)} topic + {len(micro_predictions)} micro‑topic predictions")
    print("=" * 80)


if __name__ == "__main__":
    main()