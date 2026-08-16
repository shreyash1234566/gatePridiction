"""
Add missing label mappings to canonical_taxonomy.json.
These are naming variants of labels already mapped.
"""
import json

# Additional mappings for the 90 missing labels
EXTRA_MAPPINGS = {
    # Compiler Design
    "Compiler Design::Code Optimization": {
        "Loop Optimization": "Local Optimization and Data Flow Analysis",
        "Live Variable Analysis": "Local Optimization and Data Flow Analysis",
    },
    # Digital Logic
    "Digital Logic::Sequential Circuits": {
        "State Table and State Diagram": "Sequential Circuits",
    },
    # Discrete Math
    "Discrete Mathematics::Algebraic Structures": {
        "Groups: Definition, Axioms, Properties": "Monoids and Groups",
        "Abelian Groups": "Monoids and Groups",
    },
    "Discrete Mathematics::Graph Theory": {
        "Graph Connectivity: Cut Vertices and Bridges": "Graphs (Theory): Connectivity, Matching, Coloring",
        "Spanning Trees and Number of Spanning Trees": "Graphs (Theory): Connectivity, Matching, Coloring",
        "Graph Coloring and Chromatic Number": "Graphs (Theory): Connectivity, Matching, Coloring",
        "Bipartite Graphs": "Graphs (Theory): Connectivity, Matching, Coloring",
        "Hamiltonian Paths and Circuits": "Graphs (Theory): Connectivity, Matching, Coloring",
    },
    "Discrete Mathematics::Propositional and First-Order Logic": {
        "Universal and Existential Quantification": "Propositional and First-Order Logic",
        "Logical Connectives and Truth Tables": "Propositional and First-Order Logic",
        "Satisfiability and Validity": "Propositional and First-Order Logic",
    },
    "Discrete Mathematics::Sets, Relations, Functions": {
        "Set Operations: Union, Intersection, Difference, Complement": "Sets, Relations, Functions",
        "Partial Orders and Posets (HASSE Diagrams)": "Partial Orders and Lattices",
        "Surjective (Onto) Functions": "Sets, Relations, Functions",
        "Equivalence Relations and Equivalence Classes": "Sets, Relations, Functions",
        "Injective (One-to-One) Functions": "Sets, Relations, Functions",
    },
    # Engineering Mathematics
    "Engineering Mathematics::Calculus": {
        "Techniques of Integration": "Integration",
        "Maxima and Minima (Single Variable)": "Maxima and Minima",
    },
    "Engineering Mathematics::Linear Algebra": {
        "System of Linear Equations (Gaussian Elimination)": "Systems of Linear Equations",
        "LU Decomposition": "Matrices and Determinants",
        "Singular and Non-Singular Matrices": "Matrices and Determinants",
        "Rank of a Matrix": "Matrices and Determinants",
        "Trace of a Matrix": "Matrices and Determinants",
    },
    "Engineering Mathematics::Probability and Statistics": {
        "Expected Value (Mean) of a Distribution": "Random Variables",
        "Independent Events": "Conditional Probability and Bayes Theorem",
        "Cumulative Distribution Function (CDF)": "Random Variables",
        "Sample Space and Events": "Conditional Probability and Bayes Theorem",
        "Probability Mass Function (PMF)": "Random Variables",
        "Normal (Gaussian) Distribution": "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)",
        "Random Variables: Discrete and Continuous": "Random Variables",
        "Probability Density Function (PDF)": "Random Variables",
        "Joint Probability Distributions": "Random Variables",
    },
    # General Aptitude
    "General Aptitude::Quantitative Aptitude": {
        "Sequences and Series (AP and GP)": "Numerical Computation",
        "Percentages": "Numerical Computation",
        "Permutations and Combinations (Aptitude)": "Numerical Computation",
        "Mensuration: Area and Volume": "Numerical Computation",
        "Profit and Loss": "Numerical Computation",
        "Number Systems and Divisibility": "Numerical Computation",
        "Set Theory: Venn Diagrams (Aptitude)": "Numerical Computation",
        "Time, Speed and Distance": "Numerical Computation",
        "Geometry: Circles": "Numerical Computation",
        "Mixtures and Alligation": "Numerical Computation",
    },
    "General Aptitude::Spatial Aptitude": {
        "Completion of Figures": "Reasoning and Logic",
        "Mirror Images": "Reasoning and Logic",
    },
    "General Aptitude::Verbal Ability": {
        "Word Meanings and Vocabulary": "Grammar and Vocabulary",
        "Sentence Correction and Error Identification": "Grammar and Vocabulary",
        "Idioms and Phrases": "Grammar and Vocabulary",
        "Analogies in English": "Grammar and Vocabulary",
    },
    # Operating Systems
    "Operating Systems::CPU Scheduling": {
        "FCFS Scheduling (CPU)": "CPU Scheduling",
        "CPU Scheduling: Gantt Chart Analysis": "CPU Scheduling",
        "Preemptive vs Non-Preemptive Scheduling": "CPU Scheduling",
        "Round Robin Scheduling": "CPU Scheduling",
    },
    "Operating Systems::File Systems": {
        "Inode Structure": "File Systems",
    },
    "Operating Systems::I/O and Disk Scheduling": {
        "SCAN Disk Scheduling": "File Systems",
    },
    "Operating Systems::Memory Management": {
        "Paging: Concept and Address Translation": "Memory Management (Paging, Segmentation)",
        "Multi-Level Page Table": "Memory Management (Paging, Segmentation)",
        "Thrashing": "Virtual Memory",
        "Page Fault Rate Analysis": "Virtual Memory",
    },
    # Programming and Data Structures
    "Programming and Data Structures::Arrays, Stacks, Queues, Linked Lists": {
        "Queue: Enqueue, Dequeue Operations": "Stacks and Queues",
        "Stack: Push, Pop, Peek Operations": "Stacks and Queues",
        "Stack Applications: Expression Evaluation": "Stacks and Queues",
        "Reversing a Linked List": "Linked Lists",
    },
    "Programming and Data Structures::Graphs (Data Structure Representation)": {
        "Graph Representation: Adjacency List": "Graphs (Data Structures)",
    },
    "Programming and Data Structures::Hashing": {
        "Load Factor and Rehashing": "Hashing",
    },
    "Programming and Data Structures::Programming in C": {
        "Loops in C: for, while, do-while": "Programming in C",
        "Operators and Operator Precedence in C": "Programming in C",
        "Recursion in C": "Programming in C",
        "Pointers and Arrays in C": "Programming in C",
        "Storage Classes: auto, static, extern, register": "Programming in C",
        "Structures with Pointers in C": "Programming in C",
        "Function Pointers in C": "Programming in C",
        "Structures in C": "Programming in C",
    },
    "Programming and Data Structures::Trees": {
        "Binary Tree Traversal: Inorder, Preorder, Postorder": "Trees and Binary Search Trees",
        "Binary Search Tree (BST): Properties": "Trees and Binary Search Trees",
        "Binary Tree Height and Depth": "Trees and Binary Search Trees",
        "Heap Insertion (Swim Up)": "Binary Heaps",
        "Full Binary Tree and Complete Binary Tree": "Trees and Binary Search Trees",
        "Huffman Coding Tree": "Trees and Binary Search Trees",
    },
    # Theory of Computation
    "Theory of Computation::Context-Free Languages": {
        "Ambiguous Context-Free Grammars": "Context-Free Grammars",
        "Pumping Lemma for Context-Free Languages": "Context-Free Grammars",
    },
    "Theory of Computation::Regular Languages and Finite Automata": {
        "Deterministic Finite Automata (DFA): Definition": "Deterministic and Nondeterministic Finite Automata",
        "Regular Expression to NFA (Thompson's Construction)": "Deterministic and Nondeterministic Finite Automata",
    },
    "Theory of Computation::Turing Machines and Decidability": {
        "Chomsky Hierarchy: Type 0, 1, 2, 3 Grammars": "Turing Machines",
        "Undecidability Proofs by Reduction": "Undecidability",
        "Turing Machine: Definition and Components": "Turing Machines",
        "Decision Problems for CFLs and RLs": "Turing Machines",
        "Linear Bounded Automata (LBA)": "Turing Machines",
    },
}

# Load existing taxonomy
with open("canonical_taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

# Merge extra mappings
added = 0
for pk, extra in EXTRA_MAPPINGS.items():
    if pk in taxonomy:
        for label, concept in extra.items():
            taxonomy[pk]["label_to_concept"][label] = concept
            added += 1
    else:
        print(f"WARNING: {pk} not in taxonomy!")

# Save updated
with open("canonical_taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, indent=2, ensure_ascii=False)

print(f"Added {added} extra mappings")

# Verify: count total mapped
with open("all_micro_labels.json", "r", encoding="utf-8") as f:
    all_labels = json.load(f)

mapped = 0
unmapped = 0
for pk, data in all_labels.items():
    if pk not in taxonomy:
        unmapped += len(data["micro_labels"])
        continue
    for label in data["micro_labels"]:
        if label in taxonomy[pk]["label_to_concept"]:
            mapped += 1
        else:
            unmapped += 1
            print(f"  STILL MISSING: {pk} → {label}")

print(f"\nFinal: {mapped} mapped, {unmapped} unmapped out of 449")
