"""
Analyze micro-topic label fragmentation in Q.json.
Goal: Understand how many labels are spelling variants vs genuinely different micro-topics.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
import re

def tokenize(s):
    """Break a label into normalized word tokens."""
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return set(s.split())

def jaccard(a, b):
    """Jaccard similarity between two token sets."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def main():
    with open("Q.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("canonical_taxonomy.json", "r", encoding="utf-8") as f:
        taxonomy = json.load(f)

    # Count raw labels per concept
    concept_labels = defaultdict(lambda: defaultdict(int))  # {(pk, concept): {raw_label: count}}
    for pk, entry in taxonomy.items():
        for raw_label, concept in entry["label_to_concept"].items():
            # Count occurrences in Q.json
            pass

    # Count actual occurrences in Q.json
    label_counts = Counter()
    for q in data:
        s = q.get("subject", "").strip()
        t = q.get("topic", "").strip()
        m = q.get("micro_topic", "").strip()
        label_counts[(s, t, m)] += 1

    # For each concept, find all its raw labels and their counts
    print("=" * 80)
    print("CONCEPT → RAW LABELS ANALYSIS")
    print("=" * 80)
    
    total_concepts = 0
    concepts_with_variants = 0
    merge_candidates = 0
    keep_separate = 0
    
    # Build reverse map: for each concept, which raw labels map to it?
    concept_to_labels = defaultdict(list)  # {(pk, concept): [(raw_label, count)]}
    for pk, entry in taxonomy.items():
        subj = entry["subject"]
        topic = entry["topic"]
        for raw_label, concept in entry["label_to_concept"].items():
            count = label_counts.get((subj, topic, raw_label), 0)
            concept_to_labels[(pk, concept)].append((raw_label, count))
    
    # Analyze each concept
    for (pk, concept), labels in sorted(concept_to_labels.items()):
        total_concepts += 1
        if len(labels) <= 1:
            continue
        
        concepts_with_variants += 1
        
        # Check pairwise similarity
        label_names = [l for l, c in labels]
        tokens = [tokenize(l) for l in label_names]
        
        print(f"\n{'─'*60}")
        print(f"  Concept: {concept}")
        print(f"  Topic:   {pk}")
        print(f"  Labels ({len(labels)}):")
        for l, c in sorted(labels, key=lambda x: -x[1]):
            print(f"    [{c:3d}x] {l}")
        
        # Find pairs that are likely spelling variants (high similarity)
        pairs_similar = []
        pairs_different = []
        for i in range(len(label_names)):
            for j in range(i+1, len(label_names)):
                sim = jaccard(tokens[i], tokens[j])
                if sim >= 0.35:
                    pairs_similar.append((label_names[i], label_names[j], sim))
                    merge_candidates += 1
                else:
                    pairs_different.append((label_names[i], label_names[j], sim))
                    keep_separate += 1
        
        if pairs_similar:
            print(f"  MERGE candidates (Jaccard >= 0.35):")
            for a, b, sim in pairs_similar:
                print(f"    ✓ '{a}' ↔ '{b}' (sim={sim:.2f})")
        if pairs_different:
            print(f"  KEEP SEPARATE (Jaccard < 0.35):")
            for a, b, sim in pairs_different:
                print(f"    ✗ '{a}' ↔ '{b}' (sim={sim:.2f})")

    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"  Total concepts:             {total_concepts}")
    print(f"  Concepts with >1 label:     {concepts_with_variants}")
    print(f"  Label pairs to MERGE:       {merge_candidates}")
    print(f"  Label pairs to KEEP SEPARATE: {keep_separate}")
    print(f"  Total raw labels in Q.json: {len(label_counts)}")
    print(f"  Total questions:            {len(data)}")

if __name__ == "__main__":
    main()
