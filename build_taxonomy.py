"""
Build canonical_taxonomy.json: maps all 449 raw micro-topic labels 
to 88 official GATE CS syllabus concepts.

Uses the all_micro_labels.json as input, maps each label to its 
closest canonical syllabus concept.
"""
import json
from collections import defaultdict

with open("all_micro_labels.json", "r", encoding="utf-8") as f:
    all_labels = json.load(f)

# ================================================================
# CANONICAL CONCEPT DEFINITIONS (from official GATE 2026 syllabus)
# Each topic maps to a list of canonical concepts
# ================================================================

CANONICAL_MAP = {
    # ============================================================
    # ALGORITHMS
    # ============================================================
    "Algorithms::Algorithm Design: Divide and Conquer": {
        "concepts": ["Algorithm Design: Divide and Conquer"],
        "mapping": {
            "Divide and Conquer Paradigm": "Algorithm Design: Divide and Conquer",
        }
    },
    "Algorithms::Algorithm Design: Dynamic Programming": {
        "concepts": ["Algorithm Design: Dynamic Programming"],
        "mapping": {
            "Dynamic Programming: Optimal Substructure": "Algorithm Design: Dynamic Programming",
            "Floyd-Warshall Algorithm (All-Pairs Shortest Paths)": "Algorithm Design: Dynamic Programming",
            "Longest Common Subsequence (LCS)": "Algorithm Design: Dynamic Programming",
        }
    },
    "Algorithms::Algorithm Design: Greedy": {
        "concepts": ["Algorithm Design: Greedy"],
        "mapping": {
            "Greedy Algorithm Properties": "Algorithm Design: Greedy",
        }
    },
    "Algorithms::Asymptotic Analysis": {
        "concepts": ["Asymptotic Complexity Analysis"],
        "mapping": {
            "Time Complexity Analysis": "Asymptotic Complexity Analysis",
            "Theta Notation (Θ)": "Asymptotic Complexity Analysis",
            "Best, Worst and Average Case Analysis": "Asymptotic Complexity Analysis",
            "Amortized Analysis: Aggregate Method": "Asymptotic Complexity Analysis",
            "Omega Notation (Ω)": "Asymptotic Complexity Analysis",
        }
    },
    "Algorithms::Computational Complexity": {
        "concepts": ["Asymptotic Complexity Analysis"],
        "mapping": {
            "Polynomial Time Algorithms (Class P)": "Asymptotic Complexity Analysis",
            "NP-Completeness": "Asymptotic Complexity Analysis",
            "Cook-Levin Theorem (SAT is NP-Complete)": "Asymptotic Complexity Analysis",
        }
    },
    "Algorithms::Graph Algorithms": {
        "concepts": ["Graph Traversals (BFS, DFS)", "Minimum Spanning Trees", "Shortest Path Algorithms"],
        "mapping": {
            "Kruskal's Algorithm (Minimum Spanning Tree)": "Minimum Spanning Trees",
            "Dijkstra's Algorithm (Weighted Graph)": "Shortest Path Algorithms",
            "Bellman-Ford Algorithm (Negative Weights)": "Shortest Path Algorithms",
            "Cycle Detection in Directed Graph": "Graph Traversals (BFS, DFS)",
            "Topological Sorting": "Graph Traversals (BFS, DFS)",
            "Strongly Connected Components (Kosaraju's Algorithm)": "Graph Traversals (BFS, DFS)",
            "Prim's Algorithm (Minimum Spanning Tree)": "Minimum Spanning Trees",
        }
    },
    "Algorithms::Searching and Sorting": {
        "concepts": ["Searching and Sorting"],
        "mapping": {
            "Merge Sort": "Searching and Sorting",
            "Quick Sort": "Searching and Sorting",
            "Binary Search": "Searching and Sorting",
            "Heap Sort": "Searching and Sorting",
            "Linear Search": "Searching and Sorting",
            "Bubble Sort": "Searching and Sorting",
            "Stable Sorting Algorithms": "Searching and Sorting",
        }
    },
    # ============================================================
    # COMPILER DESIGN
    # ============================================================
    "Compiler Design::Code Optimization": {
        "concepts": ["Local Optimization and Data Flow Analysis"],
        "mapping": {
            "Common Subexpression Elimination (CSE)": "Local Optimization and Data Flow Analysis",
            "Constant Folding": "Local Optimization and Data Flow Analysis",
            "Dead Code Elimination": "Local Optimization and Data Flow Analysis",
            "Control Flow Graph (CFG)": "Local Optimization and Data Flow Analysis",
            "Basic Blocks and Flow Graphs": "Local Optimization and Data Flow Analysis",
            "Reaching Definitions Analysis": "Local Optimization and Data Flow Analysis",
            "Live Variable Analysis": "Local Optimization and Data Flow Analysis",
            "Loop Optimization": "Local Optimization and Data Flow Analysis",
        }
    },
    "Compiler Design::Intermediate Code Generation": {
        "concepts": ["Intermediate Code Generation"],
        "mapping": {
            "Three-Address Code (TAC)": "Intermediate Code Generation",
            "Abstract Syntax Tree (AST)": "Intermediate Code Generation",
        }
    },
    "Compiler Design::Lexical Analysis": {
        "concepts": ["Lexical Analysis"],
        "mapping": {
            "Token Types: Keywords, Identifiers, Operators": "Lexical Analysis",
            "Keyword and Token Recognition": "Lexical Analysis",
            "Lexical Analysis: Regular Expressions for Token Specification": "Lexical Analysis",
        }
    },
    "Compiler Design::Runtime Environment": {
        "concepts": ["Runtime Environments"],
        "mapping": {
            "Activation Record (Stack Frame) Structure": "Runtime Environments",
            "Static and Dynamic Scoping": "Runtime Environments",
            "Parameter Passing Mechanisms": "Runtime Environments",
        }
    },
    "Compiler Design::Syntax Analysis (Parsing)": {
        "concepts": ["Syntax Analysis (Parsing)"],
        "mapping": {
            "LR(1) Parsing": "Syntax Analysis (Parsing)",
            "FIRST and FOLLOW Sets": "Syntax Analysis (Parsing)",
            "LL(1) Parsing": "Syntax Analysis (Parsing)",
            "Operator Precedence Parsing": "Syntax Analysis (Parsing)",
            "SLR(1) Parsing": "Syntax Analysis (Parsing)",
            "CLR(1) Parsing": "Syntax Analysis (Parsing)",
            "LALR(1) Parsing": "Syntax Analysis (Parsing)",
            "Handle and Viable Prefix in LR Parsing": "Syntax Analysis (Parsing)",
            "LR(0) Items and Canonical Collection": "Syntax Analysis (Parsing)",
            "Predictive (Top-Down) Parsing": "Syntax Analysis (Parsing)",
            "Parse Trees": "Syntax Analysis (Parsing)",
            "Ambiguous Grammars in Parsing": "Syntax Analysis (Parsing)",
            "Left Recursion Removal": "Syntax Analysis (Parsing)",
        }
    },
    "Compiler Design::Syntax-Directed Translation": {
        "concepts": ["Syntax-Directed Translation"],
        "mapping": {
            "Syntax-Directed Translation Schemes (SDT)": "Syntax-Directed Translation",
            "Synthesized and Inherited Attributes": "Syntax-Directed Translation",
            "S-Attributed and L-Attributed Definitions": "Syntax-Directed Translation",
            "Syntax-Directed Definition (SDD)": "Syntax-Directed Translation",
        }
    },
    # ============================================================
    # COMPUTER NETWORKS
    # ============================================================
    "Computer Networks::Application Layer Protocols": {
        "concepts": ["Application Layer (DNS, SMTP, HTTP, FTP)"],
        "mapping": {
            "DNS Protocol and Name Resolution": "Application Layer (DNS, SMTP, HTTP, FTP)",
            "HTTP Protocol: Request and Response": "Application Layer (DNS, SMTP, HTTP, FTP)",
            "HTTP Persistent vs Non-Persistent Connections": "Application Layer (DNS, SMTP, HTTP, FTP)",
            "Email System Architecture (MUA, MTA, MDA)": "Application Layer (DNS, SMTP, HTTP, FTP)",
            "FTP Protocol": "Application Layer (DNS, SMTP, HTTP, FTP)",
            "DHCP Protocol (Application Layer View)": "Application Layer (DNS, SMTP, HTTP, FTP)",
        }
    },
    "Computer Networks::Data Link Layer": {
        "concepts": ["Data Link Layer (Framing, Error/Flow Control, MAC)", "LAN Technologies (Ethernet)"],
        "mapping": {
            "Error Correction: Hamming Code": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Error Detection: CRC (Cyclic Redundancy Check)": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Error Detection: Parity Bits": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Ethernet (IEEE 802.3): CSMA/CD": "LAN Technologies (Ethernet)",
            "ALOHA Protocol: Pure and Slotted": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Framing Techniques: Character Stuffing, Bit Stuffing": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Stop-and-Wait ARQ": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Go-Back-N ARQ": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Token Ring (IEEE 802.5)": "LAN Technologies (Ethernet)",
            "Selective Repeat ARQ": "Data Link Layer (Framing, Error/Flow Control, MAC)",
            "Sliding Window Protocol": "Data Link Layer (Framing, Error/Flow Control, MAC)",
        }
    },
    "Computer Networks::Network Layer and IP Addressing": {
        "concepts": ["Network Layer (IPv4/IPv6, Routing Algorithms)", "IP Support Protocols (ARP, DHCP, ICMP, NAT)"],
        "mapping": {
            "IP Fragmentation and Reassembly": "Network Layer (IPv4/IPv6, Routing Algorithms)",
            "CIDR (Classless Inter-Domain Routing) and Route Aggregation": "Network Layer (IPv4/IPv6, Routing Algorithms)",
            "IPv4 Header Fields and Structure": "Network Layer (IPv4/IPv6, Routing Algorithms)",
            "IP Addressing: Classful Addressing": "Network Layer (IPv4/IPv6, Routing Algorithms)",
            "Subnetting and Subnet Masks": "Network Layer (IPv4/IPv6, Routing Algorithms)",
            "NAT (Network Address Translation)": "IP Support Protocols (ARP, DHCP, ICMP, NAT)",
            "ICMP Protocol": "IP Support Protocols (ARP, DHCP, ICMP, NAT)",
            "ARP Protocol": "IP Support Protocols (ARP, DHCP, ICMP, NAT)",
            "IPv6 Addressing and Header Format": "Network Layer (IPv4/IPv6, Routing Algorithms)",
            "Variable Length Subnet Masking (VLSM)": "Network Layer (IPv4/IPv6, Routing Algorithms)",
        }
    },
    "Computer Networks::Network Security": {
        "concepts": ["Network Security (Public Key, Digital Signatures, Firewalls)"],
        "mapping": {
            "Asymmetric (Public Key) Cryptography (RSA)": "Network Security (Public Key, Digital Signatures, Firewalls)",
            "Firewall: Packet Filtering": "Network Security (Public Key, Digital Signatures, Firewalls)",
            "Symmetric Key Cryptography (AES, DES)": "Network Security (Public Key, Digital Signatures, Firewalls)",
            "Digital Signatures and Certificates": "Network Security (Public Key, Digital Signatures, Firewalls)",
        }
    },
    "Computer Networks::Routing Protocols": {
        "concepts": ["Network Layer (IPv4/IPv6, Routing Algorithms)"],
        "mapping": {
            "Routing Algorithms: Distance Vector Routing": "Network Layer (IPv4/IPv6, Routing Algorithms)",
        }
    },
    "Computer Networks::Transport Layer": {
        "concepts": ["Transport Layer (TCP, UDP, Sockets, Congestion Control)"],
        "mapping": {
            "TCP Sequence Numbers and Acknowledgments": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "TCP Congestion Control: Slow Start": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "Socket API and Socket Programming": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "UDP Protocol: Characteristics and Uses": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "TCP Retransmission and Timeout": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "TCP Connection Establishment: Three-Way Handshake": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "TCP Flow Control: Sliding Window": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "TCP vs UDP Comparison": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
            "Port Numbers and Multiplexing": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
        }
    },
    # ============================================================
    # COMPUTER ORGANIZATION AND ARCHITECTURE
    # ============================================================
    "Computer Organization and Architecture::ALU, Data-Path and Control Unit": {
        "concepts": ["ALU, Data-path and Control Unit"],
        "mapping": {
            "Data-Path Architecture": "ALU, Data-path and Control Unit",
            "Instruction Execution Cycle (Fetch, Decode, Execute)": "ALU, Data-path and Control Unit",
            "RISC vs CISC Architecture": "ALU, Data-path and Control Unit",
            "Hardwired vs Microprogrammed Control Unit": "ALU, Data-path and Control Unit",
        }
    },
    "Computer Organization and Architecture::I/O Interface": {
        "concepts": ["I/O Interface (Interrupt and DMA)"],
        "mapping": {
            "Direct Memory Access (DMA)": "I/O Interface (Interrupt and DMA)",
            "Interrupt Priority and Handling": "I/O Interface (Interrupt and DMA)",
            "Programmed I/O (Polling)": "I/O Interface (Interrupt and DMA)",
            "I/O Bus and Peripheral Interface": "I/O Interface (Interrupt and DMA)",
            "Interrupt-Driven I/O": "I/O Interface (Interrupt and DMA)",
        }
    },
    "Computer Organization and Architecture::Instruction Pipelining": {
        "concepts": ["Instruction Pipelining"],
        "mapping": {
            "Instruction Pipelining: Concept and Stages": "Instruction Pipelining",
            "Data Hazards in Pipelining": "Instruction Pipelining",
            "Pipeline Stalls (Bubbles)": "Instruction Pipelining",
            "Control Hazards and Branch Prediction": "Instruction Pipelining",
            "Pipeline Speedup Calculation": "Instruction Pipelining",
            "Pipeline Forwarding (Data Bypassing)": "Instruction Pipelining",
        }
    },
    "Computer Organization and Architecture::Machine Instructions and Addressing Modes": {
        "concepts": ["Machine Instructions and Addressing Modes"],
        "mapping": {
            "Instruction Format and Fields": "Machine Instructions and Addressing Modes",
            "Instruction Types: Data Transfer, Arithmetic, Logic, Control": "Machine Instructions and Addressing Modes",
            "Indirect Addressing Mode": "Machine Instructions and Addressing Modes",
            "Immediate Addressing Mode": "Machine Instructions and Addressing Modes",
            "Base-Register Addressing Mode": "Machine Instructions and Addressing Modes",
        }
    },
    "Computer Organization and Architecture::Memory Hierarchy": {
        "concepts": ["Memory Hierarchy (Cache, Main Memory, Secondary Storage)"],
        "mapping": {
            "Cache Memory: Concept and Locality of Reference": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Set Associative Cache": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Direct Mapped Cache": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Fully Associative Cache": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Cache Hit Rate and Miss Rate": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Cache Block/Line Size": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Main Memory Organization": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Cache Write Policies: Write-Through, Write-Back": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Cache Replacement Policies: LRU, FIFO, LFU": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Memory Interleaving": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Virtual Memory: Address Translation": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
            "Cache Coherence": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
        }
    },
    # ============================================================
    # DATABASES
    # ============================================================
    "Databases::Entity-Relationship Model": {
        "concepts": ["ER Model"],
        "mapping": {
            "Entity Types: Strong and Weak Entities": "ER Model",
            "Attribute Types: Simple, Composite, Multivalued, Derived": "ER Model",
            "Entity, Attribute, and Relationship": "ER Model",
            "Cardinality Ratios (1:1, 1:M, M:N)": "ER Model",
        }
    },
    "Databases::File Organization and Indexing": {
        "concepts": ["File Organization and Indexing (B/B+ Trees)"],
        "mapping": {
            "B+ Tree Indexing": "File Organization and Indexing (B/B+ Trees)",
            "Heap File Organization": "File Organization and Indexing (B/B+ Trees)",
            "Primary Index (Dense and Sparse)": "File Organization and Indexing (B/B+ Trees)",
            "Clustering vs Non-Clustering Index": "File Organization and Indexing (B/B+ Trees)",
            "Hash File Organization": "File Organization and Indexing (B/B+ Trees)",
            "Sequential File Organization": "File Organization and Indexing (B/B+ Trees)",
        }
    },
    "Databases::Functional Dependencies and Normalization": {
        "concepts": ["Integrity Constraints and Normalization"],
        "mapping": {
            "Boyce-Codd Normal Form (BCNF)": "Integrity Constraints and Normalization",
            "Functional Dependencies (FD): Definition": "Integrity Constraints and Normalization",
            "Keys Derived from Functional Dependencies": "Integrity Constraints and Normalization",
            "Canonical Cover of FDs": "Integrity Constraints and Normalization",
            "Third Normal Form (3NF)": "Integrity Constraints and Normalization",
            "Lossless Join Decomposition": "Integrity Constraints and Normalization",
        }
    },
    "Databases::Relational Model and Relational Algebra": {
        "concepts": ["Relational Model and Relational Algebra", "Tuple Calculus"],
        "mapping": {
            "Selection (σ) in Relational Algebra": "Relational Model and Relational Algebra",
            "Projection (π) in Relational Algebra": "Relational Model and Relational Algebra",
            "Keys: Super Key, Candidate Key, Primary Key, Foreign Key": "Relational Model and Relational Algebra",
            "Natural Join in Relational Algebra": "Relational Model and Relational Algebra",
            "Division Operation in Relational Algebra": "Relational Model and Relational Algebra",
            "Relational Tuple Calculus": "Tuple Calculus",
            "Set Operations: Union, Intersection, Difference": "Relational Model and Relational Algebra",
            "Theta Join and Equi-Join": "Relational Model and Relational Algebra",
            "Functional Dependencies in Relational Model": "Relational Model and Relational Algebra",
            "Cartesian Product in Relational Algebra": "Relational Model and Relational Algebra",
        }
    },
    "Databases::SQL": {
        "concepts": ["SQL"],
        "mapping": {
            "SQL GROUP BY Clause": "SQL",
            "SQL IN and NOT IN": "SQL",
            "SQL Natural Join": "SQL",
            "SQL SELECT and FROM Clauses": "SQL",
            "SQL HAVING Clause": "SQL",
            "SQL Subqueries (Nested Queries)": "SQL",
            "SQL Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)": "SQL",
            "SQL Views: Definition and Usage": "SQL",
            "SQL INSERT, UPDATE, DELETE Statements": "SQL",
            "SQL ORDER BY Clause": "SQL",
        }
    },
    "Databases::Transactions and Concurrency Control": {
        "concepts": ["Transactions and Concurrency Control"],
        "mapping": {
            "Transaction Schedules": "Transactions and Concurrency Control",
            "Atomicity and Durability": "Transactions and Concurrency Control",
            "Log-Based Recovery: Undo and Redo": "Transactions and Concurrency Control",
            "Conflict Serializability": "Transactions and Concurrency Control",
            "Two-Phase Locking (2PL) Protocol": "Transactions and Concurrency Control",
            "ACID Properties of Transactions": "Transactions and Concurrency Control",
            "View Serializability": "Transactions and Concurrency Control",
            "Deadlock in Transactions (Wait-for Graph)": "Transactions and Concurrency Control",
        }
    },
    # ============================================================
    # DIGITAL LOGIC
    # ============================================================
    "Digital Logic::Boolean Algebra": {
        "concepts": ["Boolean Algebra"],
        "mapping": {
            "Boolean Function Representation (SOP, POS)": "Boolean Algebra",
            "Boolean Function Minimization": "Boolean Algebra",
            "Boolean Algebra Axioms and Identities": "Boolean Algebra",
            "DeMorgan's Theorem": "Boolean Algebra",
            "Canonical Forms: Minterms and Maxterms": "Boolean Algebra",
        }
    },
    "Digital Logic::Combinational Circuits": {
        "concepts": ["Combinational Circuits"],
        "mapping": {
            "Multiplexers (MUX)": "Combinational Circuits",
            "Full Adder": "Combinational Circuits",
            "Binary Multiplier": "Combinational Circuits",
            "Decoders": "Combinational Circuits",
            "Priority Encoders": "Combinational Circuits",
            "Half Subtractor and Full Subtractor": "Combinational Circuits",
        }
    },
    "Digital Logic::Logic Gates": {
        "concepts": ["Boolean Algebra"],
        "mapping": {
            "Gate-Level Implementation of Boolean Functions": "Boolean Algebra",
            "Universal Gates: NAND, NOR": "Boolean Algebra",
        }
    },
    "Digital Logic::Minimization": {
        "concepts": ["Minimization"],
        "mapping": {
            "Karnaugh Map (K-Map) Minimization": "Minimization",
            "Prime Implicants and Essential Prime Implicants": "Minimization",
        }
    },
    "Digital Logic::Number Systems and Computer Arithmetic": {
        "concepts": ["Number Representations and Computer Arithmetic"],
        "mapping": {
            "Number Base Conversion": "Number Representations and Computer Arithmetic",
            "IEEE 754 Floating Point Standard": "Number Representations and Computer Arithmetic",
            "Single and Double Precision Representation": "Number Representations and Computer Arithmetic",
            "2's Complement Representation": "Number Representations and Computer Arithmetic",
            "Fixed Point Arithmetic": "Number Representations and Computer Arithmetic",
            "1's Complement Representation": "Number Representations and Computer Arithmetic",
            "Binary Addition and Subtraction": "Number Representations and Computer Arithmetic",
            "Overflow Detection in Arithmetic": "Number Representations and Computer Arithmetic",
            "Signed Magnitude Representation": "Number Representations and Computer Arithmetic",
        }
    },
    "Digital Logic::Sequential Circuits": {
        "concepts": ["Sequential Circuits"],
        "mapping": {
            "D Flip-Flop": "Sequential Circuits",
            "JK Flip-Flop": "Sequential Circuits",
            "Synchronous Counters": "Sequential Circuits",
            "Finite State Machine (FSM) Design": "Sequential Circuits",
            "State Diagram and State Table": "Sequential Circuits",
            "SR Latch": "Sequential Circuits",
            "Asynchronous Counters (Ripple Counters)": "Sequential Circuits",
            "Shift Registers": "Sequential Circuits",
        }
    },
    # ============================================================
    # DISCRETE MATHEMATICS
    # ============================================================
    "Discrete Mathematics::Algebraic Structures": {
        "concepts": ["Monoids and Groups"],
        "mapping": {
            "Subgroups and Lagrange's Theorem": "Monoids and Groups",
            "Groups: Definition, Axioms, Properties, Abelian Groups": "Monoids and Groups",
            "Monoids and Semigroups": "Monoids and Groups",
        }
    },
    "Discrete Mathematics::Combinatorics": {
        "concepts": ["Combinatorics: Counting, Recurrence Relations, Generating Functions"],
        "mapping": {
            "Counting Principles: Product and Sum Rules": "Combinatorics: Counting, Recurrence Relations, Generating Functions",
            "Recurrence Relations": "Combinatorics: Counting, Recurrence Relations, Generating Functions",
            "Generating Functions": "Combinatorics: Counting, Recurrence Relations, Generating Functions",
            "Permutations": "Combinatorics: Counting, Recurrence Relations, Generating Functions",
            "Combinations and Binomial Theorem": "Combinatorics: Counting, Recurrence Relations, Generating Functions",
        }
    },
    "Discrete Mathematics::Graph Theory": {
        "concepts": ["Graphs (Theory): Connectivity, Matching, Coloring"],
        "mapping": {
            "Planar Graphs and Euler's Formula": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Graph Definitions: Vertices, Edges, Degree": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Degree Sequences and Handshaking Lemma": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Trees and Spanning Trees": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Eulerian and Hamiltonian Paths/Circuits": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Graph Isomorphism": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Graph Coloring": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Chromatic Number": "Graphs (Theory): Connectivity, Matching, Coloring",
            "Bipartite Graphs and Matchings": "Graphs (Theory): Connectivity, Matching, Coloring",
        }
    },
    "Discrete Mathematics::Propositional and First-Order Logic": {
        "concepts": ["Propositional and First-Order Logic"],
        "mapping": {
            "Propositional Logic: Syntax and Semantics": "Propositional and First-Order Logic",
            "First-Order Logic: Predicates and Quantifiers": "Propositional and First-Order Logic",
            "Tautologies and Contradictions": "Propositional and First-Order Logic",
            "Normal Forms: CNF, DNF": "Propositional and First-Order Logic",
            "Logical Equivalences and Implications": "Propositional and First-Order Logic",
            "Validity and Satisfiability of FOL": "Propositional and First-Order Logic",
        }
    },
    "Discrete Mathematics::Sets, Relations, Functions": {
        "concepts": ["Sets, Relations, Functions", "Partial Orders and Lattices"],
        "mapping": {
            "Types of Relations: Reflexive, Symmetric, Antisymmetric, Transitive": "Sets, Relations, Functions",
            "Functions: Domain, Codomain, Range": "Sets, Relations, Functions",
            "Power Sets and Cardinality": "Sets, Relations, Functions",
            "Partial Orders and Hasse Diagrams": "Partial Orders and Lattices",
            "Lattices: Definition and Properties": "Partial Orders and Lattices",
            "Equivalence Classes and Partitions": "Sets, Relations, Functions",
            "Set Theory Basics": "Sets, Relations, Functions",
            "Relations: Equivalence and Partial Order": "Partial Orders and Lattices",
        }
    },
    # ============================================================
    # ENGINEERING MATHEMATICS
    # ============================================================
    "Engineering Mathematics::Calculus": {
        "concepts": ["Limits, Continuity, Differentiability", "Integration", "Maxima and Minima"],
        "mapping": {
            "Derivatives: Rules and Applications": "Limits, Continuity, Differentiability",
            "Integration: Definite and Indefinite Integrals": "Integration",
            "Continuity and Discontinuity": "Limits, Continuity, Differentiability",
            "L'Hôpital's Rule": "Limits, Continuity, Differentiability",
            "Differentiability": "Limits, Continuity, Differentiability",
            "Limits of Functions": "Limits, Continuity, Differentiability",
            "Maxima and Minima of Functions": "Maxima and Minima",
            "Mean Value Theorem": "Limits, Continuity, Differentiability",
        }
    },
    "Engineering Mathematics::Linear Algebra": {
        "concepts": ["Matrices and Determinants", "Systems of Linear Equations", "Eigenvalues and Eigenvectors"],
        "mapping": {
            "Eigenvalues and Eigenvectors": "Eigenvalues and Eigenvectors",
            "Matrices: Types and Operations": "Matrices and Determinants",
            "Determinants and Their Properties": "Matrices and Determinants",
            "System of Linear Equations (Ax=b)": "Systems of Linear Equations",
            "Matrix Rank and Row Echelon Form": "Matrices and Determinants",
            "Diagonalization of Matrices": "Eigenvalues and Eigenvectors",
            "Matrix Inverse": "Matrices and Determinants",
            "Vector Spaces and Subspaces": "Systems of Linear Equations",
            "Cayley-Hamilton Theorem": "Eigenvalues and Eigenvectors",
        }
    },
    "Engineering Mathematics::Probability and Statistics": {
        "concepts": ["Random Variables", "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)", "Conditional Probability and Bayes Theorem", "Mean, Median, Mode, Standard Deviation"],
        "mapping": {
            "Classical Probability": "Conditional Probability and Bayes Theorem",
            "Conditional Probability": "Conditional Probability and Bayes Theorem",
            "Variance and Standard Deviation": "Mean, Median, Mode, Standard Deviation",
            "Bayes' Theorem": "Conditional Probability and Bayes Theorem",
            "Random Variables: Continuous and Discrete": "Random Variables",
            "Normal Distribution": "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)",
            "Bernoulli and Binomial Distribution": "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)",
            "Poisson Distribution": "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)",
            "Uniform Distribution": "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)",
            "Exponential Distribution": "Distributions (Uniform, Normal, Exponential, Poisson, Binomial)",
            "Mean and Median": "Mean, Median, Mode, Standard Deviation",
            "Independent and Dependent Events": "Conditional Probability and Bayes Theorem",
            "Expected Value of Random Variable": "Random Variables",
        }
    },
    # ============================================================
    # GENERAL APTITUDE
    # ============================================================
    "General Aptitude::Logical and Analytical Reasoning": {
        "concepts": ["Reasoning and Logic"],
        "mapping": {
            "Statements and Inferences": "Reasoning and Logic",
            "Syllogisms": "Reasoning and Logic",
            "Critical Reasoning and Assumptions": "Reasoning and Logic",
            "Blood Relations": "Reasoning and Logic",
            "Data Sufficiency": "Reasoning and Logic",
            "Number Series": "Reasoning and Logic",
            "Logical Puzzles": "Reasoning and Logic",
            "Analogies in Reasoning": "Reasoning and Logic",
        }
    },
    "General Aptitude::Quantitative Aptitude": {
        "concepts": ["Data Interpretation", "Numerical Computation"],
        "mapping": {
            "Algebra: Linear and Quadratic Equations": "Numerical Computation",
            "Probability in Aptitude": "Numerical Computation",
            "Geometry: Lines, Angles, Triangles": "Numerical Computation",
            "Data Interpretation: Bar Charts": "Data Interpretation",
            "Data Interpretation: Line Graphs": "Data Interpretation",
            "Data Interpretation: Pie Charts": "Data Interpretation",
            "Data Interpretation: Tables": "Data Interpretation",
            "Ratio and Proportion": "Numerical Computation",
            "Speed, Distance, and Time": "Numerical Computation",
            "Percentages and Profit/Loss": "Numerical Computation",
            "Work and Time Problems": "Numerical Computation",
            "Averages": "Numerical Computation",
            "Logarithms": "Numerical Computation",
            "Permutations and Combinations in Aptitude": "Numerical Computation",
            "Simple and Compound Interest": "Numerical Computation",
            "Number Properties (Divisibility, Remainders)": "Numerical Computation",
            "Sequences and Series (AP, GP, HP)": "Numerical Computation",
            "Set Theory in Aptitude (Venn Diagrams)": "Numerical Computation",
            "Mixtures and Alligations": "Numerical Computation",
            "Pipes and Cisterns": "Numerical Computation",
        }
    },
    "General Aptitude::Spatial Aptitude": {
        "concepts": ["Reasoning and Logic"],
        "mapping": {
            "Cube and Dice Problems": "Reasoning and Logic",
            "Paper Folding and Cutting": "Reasoning and Logic",
            "3D Shapes and Perspectives": "Reasoning and Logic",
            "Mirror and Water Image": "Reasoning and Logic",
            "Pattern Recognition and Completion": "Reasoning and Logic",
        }
    },
    "General Aptitude::Verbal Ability": {
        "concepts": ["Grammar and Vocabulary", "Reading Comprehension", "Sentence Completion"],
        "mapping": {
            "Sentence Completion and Fill in the Blanks": "Sentence Completion",
            "Reading Comprehension": "Reading Comprehension",
            "Articles (a, an, the)": "Grammar and Vocabulary",
            "Subject-Verb Agreement": "Grammar and Vocabulary",
            "Sentence Rearrangement": "Grammar and Vocabulary",
            "Synonyms and Antonyms": "Grammar and Vocabulary",
            "Paragraph Coherence": "Reading Comprehension",
            "Prepositions": "Grammar and Vocabulary",
        }
    },
    # ============================================================
    # OPERATING SYSTEMS
    # ============================================================
    "Operating Systems::CPU Scheduling": {
        "concepts": ["CPU Scheduling"],
        "mapping": {
            "Shortest Remaining Time First (SRTF) Scheduling": "CPU Scheduling",
            "Shortest Job First (SJF) Scheduling": "CPU Scheduling",
            "Priority Scheduling (Preemptive and Non-Preemptive)": "CPU Scheduling",
            "Round Robin (RR) Scheduling": "CPU Scheduling",
            "Turnaround Time and Waiting Time Calculation": "CPU Scheduling",
            "First Come First Served (FCFS) Scheduling": "CPU Scheduling",
            "Multi-Level Queue Scheduling": "CPU Scheduling",
        }
    },
    "Operating Systems::Deadlocks": {
        "concepts": ["Deadlocks"],
        "mapping": {
            "Deadlock: Necessary Conditions (Coffman's Conditions)": "Deadlocks",
            "Deadlock Detection Algorithm": "Deadlocks",
            "Banker's Algorithm": "Deadlocks",
            "Deadlock Avoidance": "Deadlocks",
            "Resource Allocation Graph (RAG)": "Deadlocks",
            "Safe State and Unsafe State": "Deadlocks",
        }
    },
    "Operating Systems::File Systems": {
        "concepts": ["File Systems"],
        "mapping": {
            "FAT File System": "File Systems",
            "Disk Buffering and Caching": "File Systems",
            "File System Structure and Layers": "File Systems",
            "Contiguous File Allocation": "File Systems",
            "Directory Structure: Single-Level, Two-Level, Tree": "File Systems",
            "Linked File Allocation": "File Systems",
            "Indexed File Allocation": "File Systems",
            "Free Space Management: Bitmap and Linked List": "File Systems",
        }
    },
    "Operating Systems::I/O and Disk Scheduling": {
        "concepts": ["File Systems"],
        "mapping": {
            "Disk Access Time: Seek Time, Rotational Latency, Transfer Time": "File Systems",
            "SSTF Disk Scheduling": "File Systems",
            "Disk Structure: Tracks, Sectors, Cylinders": "File Systems",
            "SCAN Disk Scheduling Algorithm": "File Systems",
        }
    },
    "Operating Systems::Inter-Process Communication and Synchronization": {
        "concepts": ["Concurrency and Synchronization"],
        "mapping": {
            "Semaphores: Binary and Counting": "Concurrency and Synchronization",
            "Critical Section Problem": "Concurrency and Synchronization",
            "Semaphore Wait (P) and Signal (V) Operations": "Concurrency and Synchronization",
        }
    },
    "Operating Systems::Memory Management": {
        "concepts": ["Memory Management (Paging, Segmentation)", "Virtual Memory"],
        "mapping": {
            "Page Table Structure": "Memory Management (Paging, Segmentation)",
            "Page Fault Handling": "Virtual Memory",
            "LRU Page Replacement": "Virtual Memory",
            "Paging and Page Tables": "Memory Management (Paging, Segmentation)",
            "Demand Paging": "Virtual Memory",
            "Effective Memory Access Time (Paging with TLB)": "Memory Management (Paging, Segmentation)",
            "Segmentation: Concept and Segment Table": "Memory Management (Paging, Segmentation)",
            "Optimal Page Replacement": "Virtual Memory",
            "Internal Fragmentation": "Memory Management (Paging, Segmentation)",
            "Memory Allocation Strategies: First Fit, Best Fit, Worst Fit": "Memory Management (Paging, Segmentation)",
            "Translation Lookaside Buffer (TLB)": "Memory Management (Paging, Segmentation)",
            "External Fragmentation": "Memory Management (Paging, Segmentation)",
            "FIFO Page Replacement": "Virtual Memory",
            "Fixed Partitioning and Variable Partitioning": "Memory Management (Paging, Segmentation)",
        }
    },
    "Operating Systems::Process Management": {
        "concepts": ["Processes and Threads", "System Calls"],
        "mapping": {
            "Threads: Definition and Types": "Processes and Threads",
            "Process State Transitions (New, Ready, Running, Blocked, Terminated)": "Processes and Threads",
            "Process Creation: fork() System Call": "System Calls",
            "Context Switching": "Processes and Threads",
            "Mode Switch: User Mode to Kernel Mode": "System Calls",
            "System Calls Interface": "System Calls",
            "Process Termination": "Processes and Threads",
        }
    },
    "Operating Systems::Virtual Memory": {
        "concepts": ["Virtual Memory"],
        "mapping": {
            "Virtual Memory: Concept and Benefits": "Virtual Memory",
            "Virtual Memory: Page Replacement (FIFO)": "Virtual Memory",
        }
    },
    # ============================================================
    # PROGRAMMING AND DATA STRUCTURES
    # ============================================================
    "Programming and Data Structures::Arrays, Stacks, Queues, Linked Lists": {
        "concepts": ["Arrays", "Stacks and Queues", "Linked Lists"],
        "mapping": {
            "Array Operations and Complexity": "Arrays",
            "Doubly Linked List Operations": "Linked Lists",
            "Singly Linked List Operations": "Linked Lists",
            "Stack Operations: Push, Pop, Peek": "Stacks and Queues",
            "Circular Linked List Operations": "Linked Lists",
            "Circular Queue": "Stacks and Queues",
            "Deque (Double-Ended Queue)": "Stacks and Queues",
            "Queue Operations and Complexity": "Stacks and Queues",
            "Postfix Expression Evaluation using Stack": "Stacks and Queues",
            "Merging Linked Lists": "Linked Lists",
            "Priority Queue using Heap": "Stacks and Queues",
            "Infix to Postfix Conversion": "Stacks and Queues",
        }
    },
    "Programming and Data Structures::Graphs (Data Structure Representation)": {
        "concepts": ["Graphs (Data Structures)", "Graph Traversals (BFS, DFS)"],
        "mapping": {
            "Breadth-First Search (BFS)": "Graph Traversals (BFS, DFS)",
            "Depth-First Search (DFS)": "Graph Traversals (BFS, DFS)",
            "Graph Representation: Edge List": "Graphs (Data Structures)",
            "Adjacency List Representation": "Graphs (Data Structures)",
        }
    },
    "Programming and Data Structures::Hashing": {
        "concepts": ["Hashing"],
        "mapping": {
            "Hash Functions: Division, Multiplication Methods": "Hashing",
            "Collision Handling: Separate Chaining": "Hashing",
            "Collision Handling: Double Hashing": "Hashing",
            "Collision Handling: Open Addressing (Linear Probing)": "Hashing",
        }
    },
    "Programming and Data Structures::Programming in C": {
        "concepts": ["Programming in C"],
        "mapping": {
            "C Input/Output: printf, scanf": "Programming in C",
            "Arrays in C": "Programming in C",
            "Data Types, Variables, and Constants in C": "Programming in C",
            "Pointers in C": "Programming in C",
            "Structures and Unions in C": "Programming in C",
            "Functions in C: Call by Value, Call by Reference": "Programming in C",
            "Control Structures: if-else, switch in C": "Programming in C",
            "Dynamic Memory Allocation: malloc, calloc, free": "Programming in C",
            "C Strings and String Functions": "Programming in C",
            "Bitwise Operations in C": "Programming in C",
            "Loops: for, while, do-while in C": "Programming in C",
            "Preprocessor Directives": "Programming in C",
            "File Handling in C": "Programming in C",
            "Stack and Heap Memory in C": "Programming in C",
            "Scope and Lifetime of Variables": "Programming in C",
            "Type Casting and Type Conversion": "Programming in C",
        }
    },
    "Programming and Data Structures::Recursion": {
        "concepts": ["Recursion"],
        "mapping": {
            "Recursion: Base Case and Recursive Case": "Recursion",
            "Recursive Tree and Linked-List Operations": "Recursion",
            "Tail Recursion": "Recursion",
        }
    },
    "Programming and Data Structures::Trees": {
        "concepts": ["Trees and Binary Search Trees", "Binary Heaps"],
        "mapping": {
            "Heap: Min-Heap and Max-Heap Properties": "Binary Heaps",
            "BST Search and Height Analysis": "Trees and Binary Search Trees",
            "Binary Tree: Definition and Properties": "Trees and Binary Search Trees",
            "AVL Tree Insertion and Deletion": "Trees and Binary Search Trees",
            "BST Insertion and Deletion": "Trees and Binary Search Trees",
            "Inorder, Preorder, Postorder Traversals": "Trees and Binary Search Trees",
            "Heap Operations: Insert, Delete, Heapify": "Binary Heaps",
            "B+ Tree Insertion": "Trees and Binary Search Trees",
            "B+ Trees: Properties and Operations": "Trees and Binary Search Trees",
            "Complete Binary Tree": "Trees and Binary Search Trees",
            "Pre-order and Post-order Traversal": "Trees and Binary Search Trees",
            "Red-Black Trees: Properties": "Trees and Binary Search Trees",
            "Threaded Binary Trees": "Trees and Binary Search Trees",
            "Expression Trees": "Trees and Binary Search Trees",
        }
    },
    # ============================================================
    # THEORY OF COMPUTATION
    # ============================================================
    "Theory of Computation::Closure and Decision Properties": {
        "concepts": ["Regular and Context-Free Language Properties", "Deterministic and Nondeterministic Finite Automata"],
        "mapping": {
            "Closure Properties of Regular Languages": "Regular and Context-Free Language Properties",
            "Closure Properties of Context-Free Languages": "Regular and Context-Free Language Properties",
            "Equivalence of DFA and NFA": "Deterministic and Nondeterministic Finite Automata",
        }
    },
    "Theory of Computation::Context-Free Languages": {
        "concepts": ["Context-Free Grammars", "Pushdown Automata"],
        "mapping": {
            "Context-Free Grammar (CFG): Definition and Notation": "Context-Free Grammars",
            "Pushdown Automata (PDA): Definition": "Pushdown Automata",
            "Non-Deterministic PDA (NPDA)": "Pushdown Automata",
            "Chomsky Normal Form (CNF)": "Context-Free Grammars",
            "Inherent Ambiguity in CFL": "Context-Free Grammars",
            "CFL Pumping Lemma": "Context-Free Grammars",
        }
    },
    "Theory of Computation::Regular Languages and Finite Automata": {
        "concepts": ["Regular Expressions and Regular Languages", "Deterministic and Nondeterministic Finite Automata", "Pumping Lemma"],
        "mapping": {
            "Language Accepted by DFA": "Deterministic and Nondeterministic Finite Automata",
            "Regular Expressions: Syntax and Semantics": "Regular Expressions and Regular Languages",
            "Non-Deterministic Finite Automata (NFA): Definition": "Deterministic and Nondeterministic Finite Automata",
            "DFA Minimization": "Deterministic and Nondeterministic Finite Automata",
            "NFA to DFA Conversion (Subset Construction)": "Deterministic and Nondeterministic Finite Automata",
            "Pumping Lemma for Regular Languages": "Pumping Lemma",
            "Myhill-Nerode Theorem and Equivalence Classes": "Regular Expressions and Regular Languages",
        }
    },
    "Theory of Computation::Turing Machines and Decidability": {
        "concepts": ["Turing Machines", "Undecidability"],
        "mapping": {
            "Recursive (Decidable) Languages": "Turing Machines",
            "Undecidability: Halting Problem": "Undecidability",
            "Recursively Enumerable (RE) Languages": "Turing Machines",
            "Turing Machine: Definition and Computation": "Turing Machines",
            "Universal Turing Machine": "Turing Machines",
            "Rice's Theorem": "Undecidability",
            "Reductions Between Problems": "Undecidability",
            "Multi-Tape and Non-Deterministic Turing Machines": "Turing Machines",
            "Church-Turing Thesis": "Turing Machines",
        }
    },
}

# ============================================================
# VERIFICATION: Make sure every raw label is mapped
# ============================================================
mapped_count = 0
unmapped = []
for pk, data in all_labels.items():
    if pk not in CANONICAL_MAP:
        for label in data["micro_labels"]:
            unmapped.append((pk, label))
        continue
    
    mapping = CANONICAL_MAP[pk]["mapping"]
    for label in data["micro_labels"]:
        if label in mapping:
            mapped_count += 1
        else:
            unmapped.append((pk, label))

print(f"Mapped: {mapped_count}/449")
print(f"Unmapped: {len(unmapped)}")
if unmapped:
    for pk, label in unmapped:
        print(f"  MISSING: {pk} → {label}")

# ============================================================
# BUILD OUTPUT: canonical_taxonomy.json
# ============================================================
output = {}
for pk, cm in CANONICAL_MAP.items():
    parts = pk.split("::", 1)
    subject = parts[0]
    topic = parts[1]
    
    output[pk] = {
        "subject": subject,
        "topic": topic,
        "canonical_concepts": cm["concepts"],
        "label_to_concept": cm["mapping"],
    }

with open("canonical_taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Stats
all_concepts = set()
for pk, cm in CANONICAL_MAP.items():
    for c in cm["concepts"]:
        all_concepts.add(c)
print(f"\nTotal unique canonical concepts: {len(all_concepts)}")
print(f"Compression: 449 labels → {len(all_concepts)} concepts ({449/len(all_concepts):.1f}:1)")
print(f"\nSaved canonical_taxonomy.json")
