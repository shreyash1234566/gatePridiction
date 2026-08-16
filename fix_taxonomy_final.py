"""Final batch: map ALL remaining 88 unmapped labels."""
import json

FINAL_EXTRA = {
    "Algorithms::Graph Algorithms": {
        "Topological Sort": "Graph Traversals (BFS, DFS)",
    },
    "Algorithms::Searching and Sorting": {
        "Quick Sort: Pivot Selection and Worst Case": "Searching and Sorting",
        "Selection Sort": "Searching and Sorting",
    },
    "Compiler Design::Code Optimization": {
        "Local Optimization Techniques": "Local Optimization and Data Flow Analysis",
        "Register Allocation by Graph Coloring": "Local Optimization and Data Flow Analysis",
    },
    "Compiler Design::Lexical Analysis": {
        "Role of Lexical Analyzer": "Lexical Analysis",
        "Symbol Table: Structure and Operations": "Lexical Analysis",
        "Regular Expressions in Lexical Analysis": "Lexical Analysis",
    },
    "Compiler Design::Syntax Analysis (Parsing)": {
        "Bottom-Up Parsing": "Syntax Analysis (Parsing)",
        "Parse Trees and Derivations": "Syntax Analysis (Parsing)",
        "Context-Free Grammar for Programming Languages": "Syntax Analysis (Parsing)",
        "LL(1) Parsing Table Construction": "Syntax Analysis (Parsing)",
        "Shift-Reduce Parsing": "Syntax Analysis (Parsing)",
        "Left Recursion Elimination": "Syntax Analysis (Parsing)",
        "FOLLOW Sets": "Syntax Analysis (Parsing)",
        "Predictive Parsing (LL)": "Syntax Analysis (Parsing)",
        "Ambiguous Grammar and Parsing": "Syntax Analysis (Parsing)",
        "LR(0) Parsing and Items": "Syntax Analysis (Parsing)",
    },
    "Computer Networks::Data Link Layer": {
        "Sliding Window Protocol Efficiency": "Data Link Layer (Framing, Error/Flow Control, MAC)",
        "Stop-and-Wait Protocol": "Data Link Layer (Framing, Error/Flow Control, MAC)",
        "IEEE 802.11 Wireless LAN (Wi-Fi)": "LAN Technologies (Ethernet)",
        "Framing: Bit Stuffing and Byte Stuffing": "Data Link Layer (Framing, Error/Flow Control, MAC)",
        "Token Ring Protocol": "LAN Technologies (Ethernet)",
    },
    "Computer Networks::Network Layer and IP Addressing": {
        "IP Addressing (IPv4): Classful Addressing": "Network Layer (IPv4/IPv6, Routing Algorithms)",
        "Subnet Masks and Subnetting": "Network Layer (IPv4/IPv6, Routing Algorithms)",
        "IPv6 Addressing and Header": "Network Layer (IPv4/IPv6, Routing Algorithms)",
        "IP Forwarding and Routing Tables": "Network Layer (IPv4/IPv6, Routing Algorithms)",
        "ICMP Protocol and Ping": "IP Support Protocols (ARP, DHCP, ICMP, NAT)",
    },
    "Computer Networks::Network Security": {
        "RSA Algorithm (Key Generation, Encryption, Decryption)": "Network Security (Public Key, Digital Signatures, Firewalls)",
    },
    "Computer Networks::Transport Layer": {
        "TCP Protocol: Connection-Oriented": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
        "TCP Three-Way Handshake": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
        "UDP Protocol": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
        "TCP State Machine": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
        "TCP Timer Management and RTT Estimation": "Transport Layer (TCP, UDP, Sockets, Congestion Control)",
    },
    "Computer Organization and Architecture::ALU, Data-Path and Control Unit": {
        "ALU Design and Operations": "ALU, Data-path and Control Unit",
    },
    "Computer Organization and Architecture::I/O Interface": {
        "Interrupt Service Routine (ISR)": "I/O Interface (Interrupt and DMA)",
    },
    "Computer Organization and Architecture::Instruction Pipelining": {
        "CPI (Cycles Per Instruction) Analysis": "Instruction Pipelining",
        "Data Forwarding (Bypassing)": "Instruction Pipelining",
        "Pipeline Throughput and Speedup": "Instruction Pipelining",
    },
    "Computer Organization and Architecture::Memory Hierarchy": {
        "Memory Hierarchy: Levels and Trade-offs": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
        "Write-Back Policy": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
        "Write-Through Policy": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
        "LRU Cache Replacement": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
        "Secondary Storage: HDD and SSD": "Memory Hierarchy (Cache, Main Memory, Secondary Storage)",
    },
    "Databases::Entity-Relationship Model": {
        "Cardinality Ratios: One-to-One, One-to-Many, Many-to-Many": "ER Model",
    },
    "Databases::Functional Dependencies and Normalization": {
        "First Normal Form (1NF)": "Integrity Constraints and Normalization",
    },
    "Databases::Relational Model and Relational Algebra": {
        "Tuple Relational Calculus": "Tuple Calculus",
        "Relational Schema Design": "Relational Model and Relational Algebra",
        "Relations, Tuples, and Attributes": "Relational Model and Relational Algebra",
        "Integrity Constraints: Entity Integrity, Referential Integrity": "Relational Model and Relational Algebra",
        "Outer Joins: Left, Right, Full": "Relational Model and Relational Algebra",
        "Rename (ρ) Operation": "Relational Model and Relational Algebra",
    },
    "Databases::SQL": {
        "SQL Joins: INNER, LEFT, RIGHT, FULL OUTER": "SQL",
        "SQL Aggregate Functions: COUNT, SUM, AVG, MIN, MAX": "SQL",
        "SQL SELECT Queries": "SQL",
        "SQL WHERE Clause and Predicates": "SQL",
        "SQL DDL: CREATE, ALTER, DROP": "SQL",
        "SQL EXISTS and NOT EXISTS": "SQL",
    },
    "Databases::Transactions and Concurrency Control": {
        "Two-Phase Locking (2PL)": "Transactions and Concurrency Control",
        "Serial and Serializable Schedules": "Transactions and Concurrency Control",
        "Deadlock in DBMS": "Transactions and Concurrency Control",
        "Lock-Based Protocols": "Transactions and Concurrency Control",
    },
    "Digital Logic::Boolean Algebra": {
        "Complement of Boolean Functions": "Boolean Algebra",
    },
    "Digital Logic::Number Systems and Computer Arithmetic": {
        "Sign-Magnitude Representation": "Number Representations and Computer Arithmetic",
        "Overflow Detection": "Number Representations and Computer Arithmetic",
        "Floating Point Arithmetic: Addition and Subtraction": "Number Representations and Computer Arithmetic",
        "Binary Number System": "Number Representations and Computer Arithmetic",
        "Hexadecimal Number System": "Number Representations and Computer Arithmetic",
    },
    "Digital Logic::Sequential Circuits": {
        "Modulo-N Counters": "Sequential Circuits",
        "Ring Counters and Johnson Counters": "Sequential Circuits",
        "Finite State Machine (FSM): Mealy Model": "Sequential Circuits",
        "Asynchronous (Ripple) Counters": "Sequential Circuits",
    },
}

with open("canonical_taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

added = 0
for pk, extra in FINAL_EXTRA.items():
    if pk in taxonomy:
        for label, concept in extra.items():
            taxonomy[pk]["label_to_concept"][label] = concept
            added += 1

with open("canonical_taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, indent=2, ensure_ascii=False)

print(f"Added {added} final mappings")

# Final verification
with open("all_micro_labels.json", "r", encoding="utf-8") as f:
    all_labels = json.load(f)

mapped = 0
unmapped = []
for pk, data in all_labels.items():
    if pk not in taxonomy:
        for label in data["micro_labels"]:
            unmapped.append((pk, label))
        continue
    for label in data["micro_labels"]:
        if label in taxonomy[pk]["label_to_concept"]:
            mapped += 1
        else:
            unmapped.append((pk, label))

print(f"Final: {mapped} mapped, {len(unmapped)} unmapped out of 449")
if unmapped:
    for pk, label in unmapped:
        print(f"  STILL MISSING: {pk} -> {label}")
else:
    print("ALL 449 LABELS MAPPED!")

# Count unique concepts
all_concepts = set()
for pk, data in taxonomy.items():
    for concept in data["label_to_concept"].values():
        all_concepts.add(concept)
print(f"\nTotal unique canonical concepts: {len(all_concepts)}")
