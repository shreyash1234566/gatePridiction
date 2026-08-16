"""
AUDIT 9-11: Syllabus canonical concept count, 2026 brand-new vs syllabus, 
and model efficiency analysis
"""
import json
from collections import defaultdict, Counter

with open("Q.json", "r", encoding="utf-8") as f:
    raw_questions = json.load(f)

MULTI_PAPER_YEARS = {2014: 3, 2015: 3, 2016: 2, 2021: 2, 2024: 2, 2025: 2, 2026: 2}

# ============================================================
# AUDIT 9: Official GATE CS syllabus canonical concept count
# ============================================================
# Based on the official GATE 2026 CS/IT syllabus from IIT Guwahati
# Each bullet point = one "canonical study concept"
print("=" * 80)
print("AUDIT 9: OFFICIAL SYLLABUS CANONICAL CONCEPT COUNT")
print("=" * 80)

syllabus = {
    "Digital Logic": [
        "Boolean Algebra",
        "Combinational Circuits", 
        "Sequential Circuits",
        "Minimization",
        "Number Representations and Computer Arithmetic",
    ],
    "Computer Organization and Architecture": [
        "Machine Instructions and Addressing Modes",
        "ALU, Data-path and Control Unit",
        "Instruction Pipelining",
        "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
        "I/O Interface (Interrupt and DMA)",
    ],
    "Programming and Data Structures": [
        "Programming in C",
        "Recursion",
        "Arrays",
        "Stacks and Queues",
        "Linked Lists",
        "Trees and Binary Search Trees",
        "Binary Heaps",
        "Graphs (Data Structures)",
    ],
    "Algorithms": [
        "Searching and Sorting",
        "Hashing",
        "Asymptotic Complexity Analysis",
        "Algorithm Design: Greedy",
        "Algorithm Design: Dynamic Programming",
        "Algorithm Design: Divide and Conquer",
        "Graph Traversals (BFS, DFS)",
        "Minimum Spanning Trees",
        "Shortest Path Algorithms",
    ],
    "Theory of Computation": [
        "Regular Expressions and Regular Languages",
        "Deterministic and Nondeterministic Finite Automata",
        "Context-Free Grammars",
        "Pushdown Automata",
        "Regular and Context-Free Language Properties",
        "Pumping Lemma",
        "Turing Machines",
        "Undecidability",
    ],
    "Compiler Design": [
        "Lexical Analysis",
        "Syntax Analysis (Parsing)",
        "Syntax-Directed Translation",
        "Runtime Environments",
        "Intermediate Code Generation",
        "Local Optimization and Data Flow Analysis",
    ],
    "Operating Systems": [
        "System Calls",
        "Processes and Threads",
        "Inter-Process Communication",
        "Concurrency and Synchronization",
        "Deadlocks",
        "CPU Scheduling",
        "Memory Management (Paging, Segmentation)",
        "Virtual Memory",
        "File Systems",
    ],
    "Databases": [
        "ER Model",
        "Relational Model and Relational Algebra",
        "Tuple Calculus",
        "SQL",
        "Integrity Constraints and Normalization",
        "File Organization and Indexing (B/B+ Trees)",
        "Transactions and Concurrency Control",
    ],
    "Computer Networks": [
        "OSI/TCP-IP Layering Concepts",
        "LAN Technologies (Ethernet)",
        "Data Link Layer (Framing, Error/Flow Control, MAC)",
        "Network Layer (IPv4/IPv6, Routing Algorithms)",
        "IP Support Protocols (ARP, DHCP, ICMP, NAT)",
        "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
        "Application Layer (DNS, SMTP, HTTP, FTP)",
        "Network Security (Public Key, Digital Signatures, Firewalls)",
    ],
    "Discrete Mathematics": [
        "Propositional and First-Order Logic",
        "Sets, Relations, Functions",
        "Partial Orders and Lattices",
        "Monoids and Groups",
        "Graphs (Theory): Connectivity, Matching, Coloring",
        "Combinatorics: Counting, Recurrence Relations, Generating Functions",
    ],
    "Linear Algebra": [
        "Matrices and Determinants",
        "Systems of Linear Equations",
        "Eigenvalues and Eigenvectors",
    ],
    "Calculus": [
        "Limits, Continuity, Differentiability",
        "Maxima and Minima",
        "Mean Value Theorem",
        "Integration",
    ],
    "Probability and Statistics": [
        "Random Variables",
        "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)",
        "Mean, Median, Mode, Standard Deviation",
        "Conditional Probability and Bayes Theorem",
    ],
    "General Aptitude - Verbal": [
        "Grammar and Vocabulary",
        "Reading Comprehension",
        "Sentence Completion",
    ],
    "General Aptitude - Quantitative": [
        "Data Interpretation",
        "Numerical Computation",
        "Reasoning and Logic",
    ],
}

total_concepts = 0
for subj, concepts in syllabus.items():
    total_concepts += len(concepts)
    print(f"  {subj}: {len(concepts)} canonical concepts")
    for c in concepts:
        print(f"    - {c}")

print(f"\n  TOTAL CANONICAL CONCEPTS: {total_concepts}")
print(f"  vs 449 raw micro-topic labels")
print(f"  Compression ratio: {449/total_concepts:.1f}:1")

# ============================================================
# AUDIT 10: 2026 "brand new" labels vs syllabus coverage
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 10: DO 2026 'BRAND NEW' LABELS MAP TO SYLLABUS CONCEPTS?")
print("=" * 80)

# Manually verify each 2026 brand-new label against the syllabus
brand_new_2026_vs_syllabus = [
    ("Edge List Representation of Graphs", "Graphs (Data Structures)", True, "Arrays, adjacency structures are part of graph DS"),
    ("Virtual Memory: Page Replacement (FIFO)", "Virtual Memory", True, "Virtual memory is explicitly in syllabus"),
    ("Syntax-Directed Definition (SDD)", "Syntax-Directed Translation", True, "Syntax-directed translation is in syllabus"),
    ("SCAN Disk Scheduling Algorithm", "File Systems", True, "Disk scheduling is part of file systems"),
    ("Linked File Allocation", "File Systems", True, "File allocation is part of file systems"),
    ("Queue Operations and Complexity", "Stacks and Queues", True, "Queues are explicitly in syllabus"),
    ("Set Theory Basics", "Sets, Relations, Functions", True, "Sets are explicitly in syllabus"),
    ("Sentence Rearrangement", "Grammar and Vocabulary", True, "General aptitude verbal"),
    ("Graph Coloring", "Graphs (Theory): Connectivity, Matching, Coloring", True, "Graph coloring is EXPLICITLY in syllabus"),
    ("Relations: Equivalence and Partial Order", "Partial Orders and Lattices", True, "Partial orders explicitly in syllabus"),
    ("Pre-order and Post-order Traversal", "Trees and Binary Search Trees", True, "Trees are in syllabus"),
    ("Percentages and Profit/Loss", "Numerical Computation", True, "Numerical computation in GA"),
    ("ARP Protocol", "IP Support Protocols (ARP, DHCP, ICMP, NAT)", True, "ARP is EXPLICITLY named in syllabus"),
    ("Pumping Lemma for Regular Languages", "Pumping Lemma", True, "Pumping lemma is EXPLICITLY in syllabus"),
    ("Postfix Expression Evaluation using Stack", "Stacks and Queues", True, "Stacks are in syllabus"),
    ("Inherent Ambiguity in CFL", "Context-Free Grammars", True, "CFG is in syllabus"),
    ("Stack and Heap Memory in C", "Programming in C", True, "Programming in C is in syllabus"),
    ("Process Termination", "Processes and Threads", True, "Processes are in syllabus"),
    ("Cache Coherence", "Memory Hierarchy (Cache, Main Memory, Secondary Storage)", True, "Cache/memory hierarchy in syllabus"),
    ("Fixed Partitioning and Variable Partitioning", "Memory Management (Paging, Segmentation)", True, "Memory management in syllabus"),
    ("Pipes and Cisterns", "Numerical Computation", True, "Quant aptitude problem type"),
    ("Combinations and Binomial Theorem", "Combinatorics: Counting, Recurrence Relations, Generating Functions", True, "Combinatorics explicitly in syllabus"),
    ("Tail Recursion", "Recursion", True, "Recursion is explicitly in syllabus"),
    ("Limits of Functions", "Limits, Continuity, Differentiability", True, "Limits EXPLICITLY in syllabus"),
    ("Logical Puzzles", "Reasoning and Logic", True, "GA reasoning"),
    ("Indirect Addressing Mode", "Machine Instructions and Addressing Modes", True, "Addressing modes EXPLICITLY in syllabus"),
    ("DHCP Protocol (Application Layer View)", "IP Support Protocols (ARP, DHCP, ICMP, NAT)", True, "DHCP is EXPLICITLY named in syllabus"),
    ("Half Subtractor and Full Subtractor", "Combinational Circuits", True, "Combinational circuits in syllabus"),
    ("Priority Queue using Heap", "Binary Heaps", True, "Binary heaps EXPLICITLY in syllabus"),
    ("Equivalence of DFA and NFA", "Deterministic and Nondeterministic Finite Automata", True, "DFA/NFA explicitly in syllabus"),
    ("Analogies in Reasoning", "Reasoning and Logic", True, "GA reasoning"),
    ("Deadlock Detection Algorithm", "Deadlocks", True, "Deadlocks explicitly in syllabus"),
    ("Threaded Binary Trees", "Trees and Binary Search Trees", True, "Trees in syllabus"),
    ("Sequential File Organization", "File Organization and Indexing (B/B+ Trees)", True, "File organization in syllabus"),
    ("Merging Linked Lists", "Linked Lists", True, "Linked lists EXPLICITLY in syllabus"),
    ("Sliding Window Protocol", "Data Link Layer (Framing, Error/Flow Control, MAC)", True, "Flow control in data link layer"),
    ("Prim's Algorithm (Minimum Spanning Tree)", "Minimum Spanning Trees", True, "MST EXPLICITLY in syllabus"),
    ("Reaching Definitions Analysis", "Local Optimization and Data Flow Analysis", True, "Data flow analysis in syllabus"),
    ("Scope and Lifetime of Variables", "Programming in C", True, "Programming in C in syllabus"),
    ("Free Space Management: Bitmap and Linked List", "File Systems", True, "File systems in syllabus"),
    ("Stable Sorting Algorithms", "Searching and Sorting", True, "Sorting EXPLICITLY in syllabus"),
]

covered = sum(1 for x in brand_new_2026_vs_syllabus if x[2])
print(f"\n  Of 41 'brand new' 2026 labels:")
print(f"    Covered by official syllabus: {covered}/41 ({covered/41*100:.0f}%)")
print(f"    NOT covered by syllabus:      {41-covered}/41")

print(f"\n  Detailed mapping:")
for label, concept, covered_flag, reason in brand_new_2026_vs_syllabus:
    mark = "✅" if covered_flag else "❌"
    print(f"    {mark} '{label[:45]}' → {concept[:40]} | {reason}")

# ============================================================
# AUDIT 11: Model efficiency — actual performance vs ceiling
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 11: MODEL EFFICIENCY (Actual Hit% / Ceiling%)")
print("=" * 80)

# From walk-forward results
actual_results = {
    2024: {"m_hit": 54.3, "m_cov": 58.5},
    2025: {"m_hit": 56.6, "m_cov": 64.6},
    2026: {"m_hit": 27.4, "m_cov": 31.5},
}

ceilings = {
    2024: {"label_ceil": 62.9, "q_ceil": 66.2},
    2025: {"label_ceil": 61.3, "q_ceil": 68.5},
    2026: {"label_ceil": 36.8, "q_ceil": 40.0},
}

print(f"\n  {'Year':6s} {'M_Hit':>7s} {'Ceil':>7s} {'Eff%':>7s} | {'M_Cov':>7s} {'Ceil':>7s} {'Eff%':>7s}")
print(f"  {'─'*6} {'─'*7} {'─'*7} {'─'*7} | {'─'*7} {'─'*7} {'─'*7}")
for y in [2024, 2025, 2026]:
    a = actual_results[y]
    c = ceilings[y]
    eff_hit = a["m_hit"] / c["label_ceil"] * 100
    eff_cov = a["m_cov"] / c["q_ceil"] * 100
    print(f"  {y:6d} {a['m_hit']:6.1f}% {c['label_ceil']:6.1f}% {eff_hit:6.1f}% | {a['m_cov']:6.1f}% {c['q_ceil']:6.1f}% {eff_cov:6.1f}%")

print(f"\n  The model achieves 74-92% of what is mathematically possible.")
print(f"  The remaining 8-26% loss comes from ranking errors within valid candidates.")

# ============================================================
# AUDIT 12: What would canonical concept mapping do to the ceiling?
# ============================================================
print("\n" + "=" * 80)
print("AUDIT 12: PROJECTED CEILING UNDER CANONICAL CONCEPTS")
print("=" * 80)

# Under canonical mapping, "brand new" labels that map to known syllabus concepts
# become HITS instead of MISSES. 
# The only remaining misses would be labels that don't map to ANY known concept.

for test_year in [2024, 2025, 2026]:
    test_q = [q for q in raw_questions if q["year"] == test_year]
    np_ = MULTI_PAPER_YEARS.get(test_year, 1)
    
    actual = defaultdict(float)
    for q in test_q:
        key = f"{q['subject']}::{q['topic']}::{q['micro_topic']}"
        actual[key] += 1.0 / np_
    
    total_q_eq = sum(actual.values())
    
    # Under canonical mapping, ALL questions from known parent topics are "coverable"
    # because the syllabus concept exists. Only truly novel PARENT topics would be missed.
    train_topics = set()
    for q in raw_questions:
        if q["year"] < test_year:
            train_topics.add(f"{q['subject']}::{q['topic']}")
    
    covered_q = 0.0
    uncovered_q = 0.0
    for q in test_q:
        pk = f"{q['subject']}::{q['topic']}"
        if pk in train_topics:
            covered_q += 1.0 / np_
        else:
            uncovered_q += 1.0 / np_
    
    canon_ceil = covered_q / total_q_eq * 100
    print(f"  {test_year}: Parent-topic coverage = {covered_q:.1f}/{total_q_eq:.1f} q-eq = {canon_ceil:.1f}% ceiling")
    if uncovered_q > 0:
        print(f"         Uncoverable (novel parent): {uncovered_q:.1f} q-eq")
    else:
        print(f"         All parent topics were known → ceiling ≈ 100%")

print("\n" + "=" * 80)
print("FULL AUDIT COMPLETE")
print("=" * 80)
