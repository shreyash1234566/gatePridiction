"""
GATE Q.json Topic Normalization Script
======================================
Cleans up duplicate/fragmented topic names in Q.json

Usage:
    python clean_topics.py

This script will:
1. Load Q.json
2. Normalize topic names using the same map as gate_prediction_system.py
3. Save backup to Q.json.backup.YYYYMMDDHHMMSS
4. Write cleaned data to Q.json
"""

import json
import os
from datetime import datetime
from collections import Counter

# Topic normalization map (same as in gate_prediction_system.py)
TOPIC_NORMALIZATION = {
    # Probability variants
    "Probability and Statistics": "Probability",
    "Probability Distribution": "Probability",
    "Random Variables": "Probability",
    "Conditional Probability": "Probability",
    "Bayes Theorem": "Probability",
    "Bayes' Theorem": "Probability",
    "Expected Value": "Probability",
    
    # IP/Network variants  
    "IP Header": "IPv4 Header",
    "IP Addressing": "IPv4 Addressing",
    "IPv4": "IPv4 Addressing",
    "Subnetting": "IPv4 Addressing",
    "CIDR": "IPv4 Addressing",
    
    # C Programming variants
    "Programming in C": "C Programming",
    "C Programming / Pointers": "C Programming",
    "C Pointers": "C Programming",
    "Pointers": "C Programming",
    "Pointers and Arrays": "C Programming",
    "C Programming Memory Management": "C Programming",
    "C Programming Recursion": "C Programming",
    "C Programming Strings": "C Programming",
    "C Programming Bitwise": "C Programming",
    "C Programming - Pointers/Linked Lists": "C Programming",
    "C Logic": "C Programming",
    
    # MST variants
    "Minimum Spanning Trees": "Minimum Spanning Tree",
    "MST": "Minimum Spanning Tree",
    "Prim's Algorithm": "Minimum Spanning Tree",
    "Kruskal's Algorithm": "Minimum Spanning Tree",
    
    # Parsing variants
    "Syntax Analysis": "Parsing",
    "Parsing / Syntax Analysis": "Parsing",
    "LL Parsing": "Parsing",
    "LL(1) Parsing": "Parsing",
    "LR Parsing": "Parsing",
    "LR(0) Parsing": "Parsing",
    "LR(1) Parsing": "Parsing",
    "SLR Parsing": "Parsing",
    "LALR Parsing": "Parsing",
    "Shift Reduce Parsing": "Parsing",
    
    # Graph variants
    "Graph Theory": "Graphs",
    "Graph Algorithms": "Graphs",
    "Graph Search": "Graph Traversal",
    "BFS": "Graph Traversal",
    "DFS": "Graph Traversal",
    
    # Memory variants
    "Memory Systems": "Memory Management",
    "Memory System": "Memory Management",
    "Memory": "Memory Management",
    "Memory Addressing": "Memory Management",
    "Memory Interfacing": "Memory Management",
    "Memory Hierarchy": "Cache Memory",
    
    # Cache variants
    "Cache Mapping": "Cache Memory",
    "Cache": "Cache Memory",
    
    # Paging variants
    "Page Replacement": "Paging",
    "Paging & Memory Management": "Paging",
    "Page Table": "Paging",
    "Demand Paging": "Paging",
    
    # Aptitude variants
    "Numerical Ability": "Quantitative Aptitude",
    "Numerical Computation": "Quantitative Aptitude",
    
    # Tree variants
    "Binary Trees": "Trees",
    "Tree Traversal": "Trees",
    
    # Deadlock variants
    "Deadlocks": "Deadlock",
    "Deadlock Conditions": "Deadlock",
    "Deadlock Prevention": "Deadlock",
    "Deadlock Avoidance": "Deadlock",
    "Deadlock Detection": "Deadlock",
    
    # Flip-flop variants
    "Flip-flops": "Flip-Flops",
    "Latches": "Flip-Flops",
    
    # FSM variants
    "Finite State Machines": "FSM",
    "State Machines": "FSM",
    "Mealy Machine": "FSM",
    "Moore Machine": "FSM",
    
    # Normalization variants
    "Normal Forms": "Normalization",
    "1NF": "Normalization",
    "2NF": "Normalization",
    "3NF": "Normalization",
    "BCNF": "Normalization",
}


def normalize_topic(topic):
    """Normalize topic name using the mapping"""
    if not topic:
        return topic
    topic = topic.strip()
    return TOPIC_NORMALIZATION.get(topic, topic)


def main():
    input_file = "Q.json"
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    print(f"📂 Loading {input_file}...")
    
    # Load data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   ✓ Loaded {len(data)} questions")
    
    # Count original topics
    original_topics = Counter(q.get('topic', '') for q in data)
    print(f"\n📊 Original unique topics: {len(original_topics)}")
    
    # Show what will be changed
    changes = {}
    for q in data:
        original = q.get('topic', '')
        normalized = normalize_topic(original)
        if original != normalized:
            if original not in changes:
                changes[original] = {'new': normalized, 'count': 0}
            changes[original]['count'] += 1
    
    if not changes:
        print("\n✅ No topic changes needed!")
        return
    
    print(f"\n🔄 Topics to be normalized ({len(changes)} variants):")
    for original, info in sorted(changes.items(), key=lambda x: -x[1]['count']):
        print(f"   {info['count']:3d}× \"{original}\" → \"{info['new']}\"")
    
    # Ask for confirmation
    total_affected = sum(c['count'] for c in changes.values())
    print(f"\n⚠️  This will modify {total_affected} questions across {len(changes)} topic variants.")
    confirm = input("Proceed? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Aborted")
        return
    
    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{input_file}.backup.{timestamp}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Backup saved: {backup_file}")
    
    # Apply normalization
    modified = 0
    for q in data:
        original = q.get('topic', '')
        normalized = normalize_topic(original)
        if original != normalized:
            q['topic'] = normalized
            modified += 1
    
    # Save modified data
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Count new topics
    new_topics = Counter(q.get('topic', '') for q in data)
    
    print(f"\n✅ Done!")
    print(f"   Modified: {modified} questions")
    print(f"   Topics reduced: {len(original_topics)} → {len(new_topics)}")
    print(f"   Saved to: {input_file}")


if __name__ == "__main__":
    main()
