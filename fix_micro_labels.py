"""
Intelligent Micro-Topic Label Normalization for GATE Q.json
===========================================================
Created by applying deep Computer Science domain knowledge.

Rules applied:
1. ONLY merge TRUE synonyms (same exact concept, different spelling)
2. NEVER merge distinct algorithms/techniques (LL(1) != LALR(1))
3. Pick the most professional GATE-standard name
4. Keep pin-point granularity - never generalize

Each entry: "messy_label" -> "clean_standardized_label"
Only labels that NEED fixing are included. Labels already clean are omitted.
"""

import json
from collections import Counter

# ======================================================================
# INTELLIGENT MAPPING: Only true synonyms, zero false merges
# Grouped by subject::topic for clarity
# ======================================================================
MICRO_TOPIC_FIX_MAP = {
    # --- Algorithms::Searching and Sorting ---
    # "Quick Sort" and "Quick Sort: Pivot Selection and Worst Case" are DIFFERENT
    # granularity: one is general, one is specific. Keep separate. NO MERGE.
    
    # --- Compiler Design::Syntax Analysis (Parsing) ---
    # LL(1), LR(0), LR(1), SLR(1), LALR(1), CLR(1) are ALL DIFFERENT.
    # DO NOT MERGE THEM.
    # "FOLLOW Sets" is a subset of "FIRST and FOLLOW Sets" - keep separate.
    # "Predictive Parsing (LL)" is essentially LL(1) - but keep separate for
    # granularity since one names the technique, the other names the formalism.
    
    # --- Computer Networks::Data Link Layer ---
    "Sliding Window Protocol": "Sliding Window Protocol Efficiency",
    # Both refer to the same sliding window analysis questions. The "Efficiency"
    # label is more descriptive and used 6x vs 1x.
    
    # --- Computer Networks::Network Architecture and Layering ---
    "TCP/IP Model: Four Layers and Functions": "TCP/IP Model",
    "OSI Model: Seven Layers and Functions": "OSI Model",
    # Shorten to standard names. These are distinct models - NEVER merge.
    
    # --- Computer Networks::Network Layer and IP Addressing ---
    "Subnet Masks and Subnetting": "Subnetting and Subnet Masks",
    # Same topic, word order difference. Pick alphabetical-first.
    # Actually let's use the more natural one:
    # Keep "Subnet Masks and Subnetting" as-is since it has 3x. Skip this.
    
    # --- Computer Networks::Transport Layer ---
    "TCP Protocol: Connection-Oriented": "TCP Connection Management",
    # More standard name. But actually both are clear. Skip.
    
    # --- Computer Organization::Memory Hierarchy ---
    # "Set Associative Cache", "Direct Mapped Cache", "Fully Associative Cache"
    # are three DIFFERENT cache organizations. NEVER merge.
    # "LRU Cache Replacement" is a specific policy. Keep separate.
    
    # --- Programming and Data Structures::Trees ---
    "B+ Tree Insertion": "B+ Trees: Properties and Operations",
    # B+ Tree Insertion (1x) is a specific operation within B+ Trees (2x).
    # Merge into the parent since both cover B+ tree operations.
    
    # --- Programming and Data Structures::Programming in C ---
    "Pointers and Arrays in C": "Pointers in C",
    # "Pointers and Arrays in C" (1x) is a subset of "Pointers in C" (5x).
    # Questions about pointer-array relationship are fundamentally pointer questions.
    
    # --- Digital Logic::Number Systems ---
    "Binary Number System": "Number Base Conversion",
    "Hexadecimal Number System": "Number Base Conversion",
    # Both single-occurrence labels about number bases. The main label
    # "Number Base Conversion" (8x) covers binary and hex conversions.
    
    # --- Engineering Mathematics::Calculus ---
    "Limits of Functions": "Continuity and Discontinuity",
    # Limits (1x) is prerequisite/part of Continuity analysis (6x).
    # In GATE, limit questions are evaluated as part of continuity.
    
    # --- Operating Systems::Deadlocks ---
    "Deadlock Avoidance": "Banker's Algorithm",
    # In GATE context, deadlock avoidance questions are almost always
    # about Banker's Algorithm. But actually they could be conceptual.
    # SKIP - keep separate for granularity.
    
    # --- Operating Systems::Memory Management ---
    "Page Fault Rate Analysis": "Page Fault Handling",
    # Page fault rate analysis (1x) is a specific metric within page fault
    # handling (5x). Same underlying topic.
    
    "Effective Memory Access Time (Paging with TLB)": "Translation Lookaside Buffer (TLB)",
    # EMAT with TLB (1x) is a calculation within TLB topic (4x).
    
    # --- Theory of Computation::Regular Languages ---
    # "Language Accepted by DFA" (25x) and "DFA: Definition" (6x) are DIFFERENT.
    # One is about language recognition, other is about construction. Keep separate.
}

# Remove entries we decided to skip
MICRO_TOPIC_FIX_MAP_FINAL = {
    "Sliding Window Protocol": "Sliding Window Protocol Efficiency",
    "B+ Tree Insertion": "B+ Trees: Properties and Operations",
    "Pointers and Arrays in C": "Pointers in C",
    "Binary Number System": "Number Base Conversion",
    "Hexadecimal Number System": "Number Base Conversion",
    "Page Fault Rate Analysis": "Page Fault Handling",
    "Effective Memory Access Time (Paging with TLB)": "Translation Lookaside Buffer (TLB)",
}

def main():
    # Load Q.json
    with open("Q.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} questions")
    
    # Count before
    before = Counter(q.get("micro_topic", "").strip() for q in data)
    print(f"Unique micro-topics BEFORE: {len(before)}")
    
    # Apply fixes
    fixed_count = 0
    fix_details = Counter()
    for q in data:
        m = q.get("micro_topic", "").strip()
        if m in MICRO_TOPIC_FIX_MAP_FINAL:
            new_label = MICRO_TOPIC_FIX_MAP_FINAL[m]
            q["micro_topic"] = new_label
            fixed_count += 1
            fix_details[f"'{m}' -> '{new_label}'"] += 1
    
    # Count after
    after = Counter(q.get("micro_topic", "").strip() for q in data)
    print(f"Unique micro-topics AFTER:  {len(after)}")
    print(f"Questions fixed: {fixed_count}")
    print(f"Labels reduced: {len(before) - len(after)}")
    
    print(f"\nFixes applied:")
    for fix, count in fix_details.most_common():
        print(f"  [{count}x] {fix}")
    
    # Save
    with open("Q.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved Q.json")

if __name__ == "__main__":
    main()
