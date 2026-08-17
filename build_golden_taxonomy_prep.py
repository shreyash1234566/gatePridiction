import json
from collections import defaultdict

def main():
    with open("Q.json", "r", encoding="utf-8") as f:
        q_data = json.load(f)

    with open("canonical_taxonomy.json", "r", encoding="utf-8") as f:
        tax_data = json.load(f)

    # 1. Reverse map from micro_topic -> Concept using canonical taxonomy
    micro_to_concept = {}
    for key, val in tax_data.items():
        subject = val["subject"]
        topic = val["topic"]
        for label, concept in val.get("label_to_concept", {}).items():
            micro_to_concept[f"{subject}::{topic}::{label}"] = concept

    # 2. Analyze the current Q.json distributions
    unmapped_labels = set()
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    for q in q_data:
        subj = q["subject"]
        top = q["topic"]
        mt = q.get("micro_topic", "")

        # Determine concept
        concept = micro_to_concept.get(f"{subj}::{top}::{mt}")
        if not concept:
            # Fallback if unmapped
            concept = "UNMAPPED_CONCEPT"
            unmapped_labels.add(f"{subj}::{top}::{mt}")

        hierarchy[subj][top][concept].add(mt)

    # Write full dump to review
    with open("hierarchy_analysis.json", "w", encoding="utf-8") as f:
        dump_hierarchy = {}
        for s in hierarchy:
            dump_hierarchy[s] = {}
            for t in hierarchy[s]:
                dump_hierarchy[s][t] = {}
                for c in hierarchy[s][t]:
                    dump_hierarchy[s][t][c] = list(hierarchy[s][t][c])
        json.dump(dump_hierarchy, f, indent=4)

    print(f"Total unmapped micro-topics (will require manual/AI assignment to golden concepts): {len(unmapped_labels)}")
    print("Hierarchy saved to hierarchy_analysis.json")

if __name__ == "__main__":
    main()
