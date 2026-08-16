import json

add_dict = {
  "Algorithms::Algorithm Design: Divide and Conquer": ["Binary Search Applications", "Matrix Multiplication (Strassen's)", "Closest Pair Problem", "Maximum Subarray Problem", "Median Finding Algorithm"],
  "Algorithms::Algorithm Design: Dynamic Programming": ["Matrix Chain Multiplication", "0/1 Knapsack Problem", "Edit Distance", "Travelling Salesman Problem (DP)", "Bellman Equation", "Overlapping Subproblems", "Coin Change Problem"],
  "Algorithms::Algorithm Design: Greedy": ["Activity Selection Problem", "Huffman Coding", "Fractional Knapsack Problem", "Job Scheduling with Deadlines", "Greedy vs Dynamic Programming"],
  "Algorithms::Asymptotic Analysis": ["Master Theorem", "Recurrence Relations (Substitution Method)", "Space Complexity Analysis", "Big-O Notation", "Amortized Analysis: Accounting Method", "Amortized Analysis: Potential Method"],
  "Algorithms::Computational Complexity": ["NP-Hard Problems", "Reductions Between Problems", "Approximation Algorithms", "Complexity Classes (coNP, PSPACE)"],
  "Algorithms::Graph Algorithms": ["Maximum Flow (Ford-Fulkerson)", "Minimum Cut Theorem", "Bipartite Graph Matching", "Articulation Points and Bridges", "Network Flow Algorithms"],
  "Algorithms::Searching and Sorting": ["Counting Sort", "Radix Sort", "Bucket Sort", "Lower Bound for Comparison Sorting (Ω(n log n))", "Interpolation Search", "Order Statistics"],

  "Compiler Design::Code Optimization": ["Strength Reduction", "Peephole Optimization", "Copy Propagation", "Available Expressions Analysis", "Inlining"],
  "Compiler Design::Intermediate Code Generation": ["Postfix Notation", "Static Single Assignment (SSA)", "Directed Acyclic Graph (DAG) for Expressions"],
  "Compiler Design::Lexical Analysis": ["NFA to DFA Conversion for Lexical Analysis", "Longest Match Rule", "Input Buffering"],
  "Compiler Design::Runtime Environments": ["Heap Memory Management", "Garbage Collection", "Storage Allocation Strategies"],
  "Compiler Design::Runtime Environment": ["Heap Memory Management", "Garbage Collection", "Storage Allocation Strategies"],
  "Compiler Design::Semantic Analysis and Intermediate Code": ["Type Checking", "Type Systems (Static/Dynamic)", "Backpatching"],
  "Compiler Design::Syntax Analysis (Parsing)": ["Error Recovery in Parsing", "Dangling Else Problem", "Chomsky Normal Form for Parsing"],
  "Compiler Design::Syntax-Directed Translation": ["Annotated Parse Trees", "Dependency Graphs"],

  "Computer Networks::Application Layer Protocols": ["SNMP Protocol", "POP3/IMAP Protocols", "Web Caching and CDN", "REST vs SOAP"],
  "Computer Networks::Data Link Layer": ["PPP Protocol", "HDLC Protocol", "VLAN (IEEE 802.1Q)", "Spanning Tree Protocol", "Bridge Learning"],
  "Computer Networks::Network Architecture and Layering": ["Encapsulation and PDU", "Protocol Data Units at Each Layer"],
  "Computer Networks::Network Layer and IP Addressing": ["Multicast Addressing", "OSPF Protocol", "BGP Protocol", "Tunneling (IPv6 over IPv4)"],
  "Computer Networks::Network Security": ["Diffie-Hellman Key Exchange", "SSL/TLS Protocol", "MD5/SHA Hash Functions", "Man-in-the-Middle Attack Prevention", "Digital Certificates and CA"],
  "Computer Networks::Routing Protocols": ["Link State Routing", "Dijkstra's Algorithm for Routing", "Count-to-Infinity Problem", "Path Vector Routing"],
  "Computer Networks::Transport Layer": ["TCP Fast Retransmit", "TCP AIMD Algorithm", "Congestion Avoidance (Tahoe/Reno)", "Selective Acknowledgment (SACK)"],

  "Computer Organization and Architecture::ALU, Data-Path and Control Unit": ["Microprogrammed Control", "Hardwired Control Unit", "ALU Design", "Booth's Algorithm for Multiplication"],
  "Computer Organization and Architecture::I/O Interface": ["Memory-Mapped I/O vs Port-Mapped I/O", "Interrupt Priority Schemes", "Daisy Chain Priority"],
  "Computer Organization and Architecture::Instruction Pipelining": ["Pipeline Stalls", "Forwarding/Bypassing", "Branch Prediction", "Superscalar architectures", "Out-of-Order Execution"],
  "Computer Organization and Architecture::Machine Instructions and Addressing Modes": ["RISC vs CISC Architecture", "Stack-Based Architecture", "Addressing Modes: Base-Register", "Indexed"],
  "Computer Organization and Architecture::Memory Hierarchy": ["Cache Coherence Protocols (MESI)", "Write Policies (Write-Through/Write-Back)", "Virtual Memory and TLB Integration", "Cache Line Replacement Policies (LRU/FIFO)"],

  "Databases::Entity-Relationship Model": ["Generalization and Specialization", "Weak Entity Sets", "Participation Constraints", "ER to Relational Model Mapping"],
  "Databases::File Organization and Indexing": ["Clustered vs Non-Clustered Index", "Hashing in File Organization (Extendible/Linear)", "Cost Analysis of Index Operations"],
  "Databases::Functional Dependencies and Normalization": ["Armstrong's Axioms", "Canonical Cover", "4NF (Fourth Normal Form)", "Lossless-Join Decomposition", "Dependency Preservation"],
  "Databases::Relational Model and Relational Algebra": ["Division Operation", "Domain Relational Calculus", "Query Equivalence"],
  "Databases::SQL": ["Triggers and Assertions", "Views and Materialized Views", "Stored Procedures", "HAVING Clause", "Window Functions"],
  "Databases::Transactions and Concurrency Control": ["Timestamp-Based Ordering", "Multi-Version Concurrency Control (MVCC)", "Distributed Transactions", "Recovery Techniques (ARIES)"],

  "Digital Logic::Boolean Algebra": ["Shannon Expansion", "Dual of Boolean Expression", "Consensus Theorem", "Complete Set of Operations (NAND/NOR)"],
  "Digital Logic::Combinational Circuits": ["Priority Encoder", "Comparator Circuit", "BCD Adder", "Look-Ahead Carry Adder", "ALU Design from Combinational Logic"],
  "Digital Logic::Logic Gates": ["Universal Gates (NAND/NOR)", "Gate-Level Minimization", "Propagation Delay"],
  "Digital Logic::Minimization": ["Quine-McCluskey Method", "Prime Implicants", "Essential Prime Implicants", "Don't-Care Conditions"],
  "Digital Logic::Number Systems and Computer Arithmetic": ["Booth's Multiplication Algorithm", "Restoring/Non-Restoring Division", "BCD Arithmetic", "Excess-3 Code"],
  "Digital Logic::Sequential Circuits": ["Mealy vs Moore Machine Conversion", "State Assignment Techniques", "Pulse-Triggered vs Edge-Triggered", "Race Condition in Flip-Flops"],

  "Discrete Mathematics::Algebraic Structures": ["Rings and Fields", "Homomorphism and Isomorphism", "Normal Subgroups", "Permutation Groups", "Cayley's Theorem"],
  "Discrete Mathematics::Combinatorics": ["Pigeonhole Principle", "Derangements", "Catalan Numbers", "Stirling Numbers", "Burnside's Lemma"],
  "Discrete Mathematics::Graph Theory": ["Graph Isomorphism", "Hamiltonian Cycle", "Kuratowski's Theorem", "Five-Color Theorem", "Network Flow in Graphs"],
  "Discrete Mathematics::Propositional and First-Order Logic": ["Resolution Principle", "Skolemization", "Prenex Normal Form", "Herbrand's Theorem", "Proof by Contradiction"],
  "Discrete Mathematics::Sets, Relations, Functions": ["Equivalence Relations and Partitions", "Total and Partial Orders", "Boolean Lattices", "Hasse Diagrams", "Well-Ordering Principle"],

  "Engineering Mathematics::Calculus": ["Taylor/Maclaurin Series", "Multiple Integrals", "Line Integrals", "Green's/Stokes' Theorem"],
  "Engineering Mathematics::Linear Algebra": ["Cayley-Hamilton Theorem", "Orthogonalization (Gram-Schmidt)", "Diagonalization", "Singular Value Decomposition", "QR Decomposition"],
  "Engineering Mathematics::Probability and Statistics": ["Chebyshev's Inequality", "Central Limit Theorem", "Hypothesis Testing", "Confidence Intervals", "Markov/Poisson Process"],

  "General Aptitude::Logical and Analytical Reasoning": ["Coding-Decoding Problems", "Blood Relations", "Seating Arrangements", "Logical Puzzles"],
  "General Aptitude::Quantitative Aptitude": ["Time and Work Problems", "Speed and Distance Problems", "Mixtures and Alligation", "Pipes and Cisterns", "Profit and Loss"],
  "General Aptitude::Spatial Aptitude": ["Mirror and Water Images", "Paper Folding Problems", "Cubes and Dice", "3D Visualization"],
  "General Aptitude::Verbal Ability": ["Analogy Questions", "Antonyms and Synonyms", "Parajumbles", "Critical Reasoning"],

  "Operating Systems::CPU Scheduling": ["Multilevel Feedback Queue", "Real-Time Scheduling (EDF, Rate Monotonic)", "Convoy Effect"],
  "Operating Systems::Deadlocks": ["Banker's Algorithm (Safety Algorithm)", "Wait-Die and Wound-Wait Schemes", "Ostrich Algorithm"],
  "Operating Systems::File Systems": ["Journaling File Systems", "File Allocation Methods (Contiguous/Linked/Indexed)", "Free Space Management"],
  "Operating Systems::I/O and Disk Scheduling": ["LOOK and C-LOOK Algorithms", "RAID Levels", "I/O Buffering"],
  "Operating Systems::Inter-Process Communication and Synchronization": ["Monitors", "Reader-Writer Problem", "Dining Philosophers Problem", "Peterson's Algorithm", "Mutex vs Semaphore"],
  "Operating Systems::Memory Management": ["Buddy System Allocation", "Memory Compaction", "Inverted Page Table", "Segmentation with Paging"],
  "Operating Systems::Process Management": ["Process State Diagram (5-State/7-State)", "Context Switching", "fork() System Call", "User-Level vs Kernel-Level Threads"],
  "Operating Systems::Virtual Memory": ["Thrashing Prevention", "Working Set Model", "Belady's Anomaly", "Demand Paging Cost Analysis"],

  "Programming and Data Structures::Arrays, Stacks, Queues, Linked Lists": ["Double-Ended Queue (Deque)", "Circular Queue", "Skip Lists", "Infix to Postfix Conversion"],
  "Programming and Data Structures::Graphs (Data Structure Representation)": ["Adjacency Matrix vs Adjacency List Comparison", "Weighted Graph Representation", "Graph Coloring Applications"],
  "Programming and Data Structures::Hashing": ["Cuckoo Hashing", "Universal Hashing", "Bloom Filters", "Perfect Hashing"],
  "Programming and Data Structures::Programming in C": ["Dynamic Memory Allocation (malloc/calloc)", "Function Pointers", "Bit Manipulation Operations", "Macro vs Function", "Volatile and Static Keywords", "String Manipulation Functions"],
  "Programming and Data Structures::Recursion": ["Tail Recursion Optimization", "Recursion vs Iteration", "Tower of Hanoi", "Recursive Tree Traversals"],
  "Programming and Data Structures::Trees": ["Red-Black Trees", "AVL Tree Rotations", "Trie Data Structure", "B-Tree Operations", "Segment Trees"],

  "Theory of Computation::Closure and Decision Properties": ["Closure Under Union/Intersection/Complement", "Decidability of Membership/Emptiness/Equivalence", "Myhill-Nerode Theorem"],
  "Theory of Computation::Context-Free Languages": ["CYK Algorithm", "Pumping Lemma for CFLs", "Chomsky Normal Form Conversion", "Greibach Normal Form"],
  "Theory of Computation::Regular Languages and Finite Automata": ["DFA Minimization (Partition Method)", "NFA to DFA Subset Construction", "Moore to Mealy Conversion", "Two-Way Finite Automata", "Epsilon-Closure"],
  "Theory of Computation::Turing Machines and Decidability": ["Rice's Theorem Applications", "PCP (Post Correspondence Problem)", "Recursively Enumerable Languages", "Multi-tape Turing Machines", "Church-Turing Thesis"]
}

with open('canonical_taxonomy.json', 'r', encoding='utf-8') as f:
    tax = json.load(f)

syllabus = {}
for pk, data in tax.items():
    subject = data.get('subject')
    topic = data.get('topic')
    seen_labels = list(data.get('label_to_concept', {}).keys())

    if subject not in syllabus:
        syllabus[subject] = {}

    combined = set(seen_labels)
    if pk in add_dict:
        combined.update(add_dict[pk])

    syllabus[subject][topic] = sorted(list(combined))

for pk, adds in add_dict.items():
    parts = pk.split("::")
    subject = parts[0]
    topic = parts[1]
    if subject not in syllabus:
        syllabus[subject] = {}
    if topic not in syllabus[subject]:
        syllabus[subject][topic] = sorted(list(adds))

with open('gate_syllabus.json', 'w', encoding='utf-8') as f:
    json.dump(syllabus, f, indent=2, ensure_ascii=False)
