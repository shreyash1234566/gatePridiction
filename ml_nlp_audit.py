import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

def clean_text(text):
    if not text:
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

def main():
    # Load data
    with open("Q_unified.json", "r", encoding="utf-8") as f:
        q_data = json.load(f)

    with open("golden_taxonomy.json", "r", encoding="utf-8") as f:
        golden = json.load(f)

    # Build reference text for each concept/microtopic
    # Use golden taxonomy structure to build a keyword profile
    profiles = {}
    for subj, concepts in golden.items():
        for concept, data in concepts.items():
            profiles[f"{subj}::{concept}"] = clean_text(concept + " " + " ".join(data["micro_topics"]))

    # Add historical text strictly from 2011-2020 to build strong profiles
    for q in q_data:
        if q["year"] <= 2020:
            key = f"{q['subject']}::{q.get('topic', '')}"
            if key in profiles:
                profiles[key] += " " + clean_text(q.get("question_text", ""))

    # Vectorize
    all_keys = list(profiles.keys())
    all_texts = list(profiles.values())

    if not all_texts:
        print("Empty text corpora")
        return

    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.9, min_df=2)
    vectorizer.fit(all_texts)
    profile_vectors = vectorizer.transform(all_texts)

    # Process all 1621 questions to find Delta
    audit_report = []

    for q in q_data:
        q_text = clean_text((q.get("question_text", "") or "") + " " + str(q.get("choices", "")))
        if not q_text.strip():
            continue

        original_key = f"{q['subject']}::{q.get('topic', '')}"

        # Check similarity
        q_vec = vectorizer.transform([q_text])
        sims = cosine_similarity(q_vec, profile_vectors)[0]

        best_idx = sims.argmax()
        best_key = all_keys[best_idx]
        best_sim = sims[best_idx]

        orig_idx = all_keys.index(original_key) if original_key in all_keys else -1
        orig_sim = sims[orig_idx] if orig_idx != -1 else 0.0

        # Flag major discrepancies
        # If the best match is significantly better than the original label's match
        # AND they are in the same subject (to prevent completely random drifts)
        subj_prefix = q['subject'] + "::"
        if best_sim > (orig_sim + 0.15) and best_key.startswith(subj_prefix) and best_key != original_key:
            audit_report.append({
                "year": q["year"],
                "subject": q["subject"],
                "question": q_text[:100] + "...",
                "old_concept": q.get("topic", "N/A"),
                "old_micro": q.get("micro_topic", "N/A"),
                "predicted_concept": best_key.replace(subj_prefix, ""),
                "orig_sim": float(orig_sim),
                "new_sim": float(best_sim)
            })

    with open("full_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(audit_report, f, indent=4)

    print(f"Audit completed for all {len(q_data)} questions (2011-2026).")
    print(f"Found {len(audit_report)} extremely severe mismatches.")

if __name__ == "__main__":
    main()
