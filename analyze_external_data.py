"""
GATE External Data Analysis Script
===================================
Analyzes external GATE datasets and compares with our Q.json

Datasets Found:
1. Biraj2004/GATE_CS-2026_Analysis - Has marks distribution 2019-2025
2. Our Q.json - Has 1,476 questions from 2011-2025
"""

import json
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from pathlib import Path

# ==================================================
# 1. DATA FROM BIRAJ'S ANALYSIS (2019-2025)
# ==================================================
# Extracted from index.html - marks by subject per year

EXTERNAL_DATA = {
    "subjects": [
        "Engineering & Discrete Mathematics", "Digital Logic", "Computer Organization & Architecture",
        "Programming & Data Structures", "Algorithms", "Theory of Computation",
        "Compiler Design", "Operating Systems", "Databases (DBMS)", "Computer Networks"
    ],
    "years": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "marks": {
        "Engineering & Discrete Mathematics": [15, 14, 16, 14, 14, 14, 12],
        "Digital Logic": [5, 5, 6, 5, 8, 5, 6],
        "Computer Organization & Architecture": [8, 10, 11, 8, 8, 9, 12],
        "Programming & Data Structures": [12, 9, 6, 7, 9, 6, 12],
        "Algorithms": [8, 9, 9, 5, 8, 9, 8],
        "Theory of Computation": [8, 9, 11, 6, 8, 7, 7],
        "Compiler Design": [6, 4, 6, 4, 8, 8, 6],
        "Operating Systems": [8, 10, 5, 8, 9, 10, 7],
        "Databases (DBMS)": [8, 8, 8, 7, 5, 8, 9],
        "Computer Networks": [7, 7, 7, 11, 8, 9, 6]
    },
    "topicwise": {
        "Engineering & Discrete Mathematics": {"Discrete Maths (Graph, Logic, Combinatorics)": 8, "Linear Algebra": 3, "Probability": 2, "Calculus": 2},
        "Digital Logic": {"Combinational Circuits": 2, "Sequential Circuits": 2, "Number Representation & Minimization": 2},
        "Computer Organization & Architecture": {"Pipelining & Hazards": 3, "Memory Hierarchy & Cache": 4, "ALU & Data Path": 2},
        "Programming & Data Structures": {"Programming (C, Recursion)": 3, "Data Structures (Trees, Heaps, Graphs)": 4, "Stacks, Queues, Lists": 2},
        "Algorithms": {"Asymptotic Analysis": 2, "Graph Algorithms (MST, Shortest Path)": 3, "Algorithm Design (Greedy, DP)": 3, "Searching & Sorting": 1},
        "Theory of Computation": {"Regular Languages & Finite Automata": 3, "Context-Free Languages & PDA": 3, "Undecidability & Turing Machines": 2},
        "Compiler Design": {"Parsing (LR, SLR)": 3, "Syntax Directed Translation": 2, "Lexical Analysis & Optimization": 1},
        "Operating Systems": {"CPU Scheduling": 2, "Memory Management & Paging": 3, "Synchronization & Deadlocks": 3, "File Systems": 1},
        "Databases (DBMS)": {"SQL & Relational Algebra": 3, "Normalization & FDs": 2, "Transactions & Concurrency": 2, "Indexing": 1},
        "Computer Networks": {"IP Addressing & Routing": 3, "TCP/UDP & Congestion Control": 3, "Application Layer Protocols": 2, "Data Link Layer": 1}
    }
}

# Subject name mapping (External -> Our format)
SUBJECT_MAP = {
    "Engineering & Discrete Mathematics": "Engineering Mathematics",
    "Digital Logic": "Digital Logic",
    "Computer Organization & Architecture": "Computer Organization",
    "Programming & Data Structures": ["Programming", "Data Structures"],
    "Algorithms": "Algorithms",
    "Theory of Computation": "Theory of Computation",
    "Compiler Design": "Compiler Design",
    "Operating Systems": "Operating Systems",
    "Databases (DBMS)": "Databases",
    "Computer Networks": "Computer Networks"
}

def analyze_external_data():
    """Analyze the external GATE analysis data"""
    print("=" * 70)
    print("EXTERNAL DATA ANALYSIS (Biraj2004/GATE_CS-2026_Analysis)")
    print("=" * 70)
    print(f"\nYears Covered: {EXTERNAL_DATA['years']}")
    print(f"Total Subjects: {len(EXTERNAL_DATA['subjects'])}")
    
    # Calculate averages
    print("\n📊 Subject-wise Average Marks (2019-2025):")
    print("-" * 50)
    subject_avgs = {}
    for subject in EXTERNAL_DATA['subjects']:
        marks = EXTERNAL_DATA['marks'][subject]
        avg = np.mean(marks)
        std = np.std(marks)
        trend = "↑" if marks[-1] > marks[0] else ("↓" if marks[-1] < marks[0] else "→")
        subject_avgs[subject] = avg
        print(f"  {trend} {subject:<45s}: {avg:5.1f} ± {std:.1f}")
    
    print(f"\n  Total Marks per Paper: {sum(subject_avgs.values()):.0f}")
    
    # Year-over-year changes
    print("\n📈 Year-over-Year Trends:")
    print("-" * 50)
    for subject in EXTERNAL_DATA['subjects']:
        marks = EXTERNAL_DATA['marks'][subject]
        changes = [marks[i+1] - marks[i] for i in range(len(marks)-1)]
        recent_trend = np.mean(marks[-3:]) - np.mean(marks[:3])
        status = "RISING" if recent_trend > 1 else ("FALLING" if recent_trend < -1 else "STABLE")
        print(f"  {subject[:40]:<40s}: {status}")
    
    # Topic analysis
    print("\n🎯 Key Topics by Subject:")
    print("-" * 50)
    for subject, topics in EXTERNAL_DATA['topicwise'].items():
        print(f"\n  {subject}:")
        for topic, marks in sorted(topics.items(), key=lambda x: -x[1]):
            print(f"    • {topic}: {marks} marks avg")
    
    return subject_avgs


def load_our_data(filepath="Q.json"):
    """Load and analyze our Q.json data"""
    print("\n" + "=" * 70)
    print("OUR Q.JSON ANALYSIS")
    print("=" * 70)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\nTotal Questions: {len(data)}")
    
    # Year distribution
    years = Counter(q.get('year') for q in data)
    print(f"Years Covered: {min(years.keys())} - {max(years.keys())}")
    
    # Subject distribution
    subjects = Counter(q.get('subject') for q in data)
    print("\n📊 Subject Distribution:")
    print("-" * 50)
    for subject, count in sorted(subjects.items(), key=lambda x: -x[1]):
        print(f"  {subject:<35s}: {count:4d} questions")
    
    # Focus on 2019-2025 to compare with external data
    recent = [q for q in data if q.get('year') and 2019 <= q.get('year') <= 2025]
    print(f"\n📅 Questions from 2019-2025: {len(recent)}")
    
    # Year-by-year for 2019-2025
    print("\n📈 Questions per Year (2019-2025):")
    for year in range(2019, 2026):
        count = sum(1 for q in data if q.get('year') == year)
        marks_est = count * 1.5  # Rough estimate (mix of 1 and 2 mark questions)
        print(f"  {year}: {count:3d} questions (~{marks_est:.0f} marks)")
    
    return data


def compare_datasets(external_avgs, our_data):
    """Compare external analysis with our data"""
    print("\n" + "=" * 70)
    print("COMPARISON: External vs Our Data")
    print("=" * 70)
    
    # Get our subject counts for 2019-2025
    our_counts = defaultdict(lambda: defaultdict(int))
    for q in our_data:
        year = q.get('year')
        subject = q.get('subject')
        if year and 2019 <= year <= 2025 and subject:
            our_counts[subject][year] += 1
    
    print("\n📊 Subject Comparison (2019-2025 Avg):")
    print("-" * 70)
    print(f"  {'Subject':<35s} | {'External Marks':<15s} | {'Our Questions':<15s}")
    print("-" * 70)
    
    for ext_subject, our_subject in SUBJECT_MAP.items():
        ext_avg = external_avgs.get(ext_subject, 0)
        
        if isinstance(our_subject, list):
            # Combined subject
            our_count = sum(sum(our_counts[s].values()) for s in our_subject) / 7
            our_subject_name = " + ".join(our_subject)
        else:
            our_count = sum(our_counts[our_subject].values()) / 7
            our_subject_name = our_subject
        
        print(f"  {our_subject_name:<35s} | {ext_avg:>10.1f} marks | {our_count:>10.1f} q/yr")
    
    # Key insights
    print("\n💡 KEY INSIGHTS:")
    print("-" * 70)
    
    # Rising subjects
    print("\n  📈 RISING SUBJECTS (based on external data):")
    for subject in EXTERNAL_DATA['subjects']:
        marks = EXTERNAL_DATA['marks'][subject]
        if marks[-1] > marks[-3] and marks[-1] > np.mean(marks[:3]):
            print(f"     • {subject}: {marks[-3]} → {marks[-1]} marks")
    
    # Falling subjects
    print("\n  📉 FALLING SUBJECTS:")
    for subject in EXTERNAL_DATA['subjects']:
        marks = EXTERNAL_DATA['marks'][subject]
        if marks[-1] < marks[-3] and marks[-1] < np.mean(marks[:3]):
            print(f"     • {subject}: {marks[-3]} → {marks[-1]} marks")
    
    # High importance topics
    print("\n  🎯 TOP TOPICS TO FOCUS (4+ marks avg):")
    all_topics = []
    for subject, topics in EXTERNAL_DATA['topicwise'].items():
        for topic, marks in topics.items():
            all_topics.append((subject, topic, marks))
    
    for subject, topic, marks in sorted(all_topics, key=lambda x: -x[2])[:10]:
        print(f"     • {topic} ({subject[:25]}): {marks} marks")


def generate_recommendations():
    """Generate preparation recommendations based on analysis"""
    print("\n" + "=" * 70)
    print("🎓 GATE 2026 PREPARATION RECOMMENDATIONS")
    print("=" * 70)
    
    print("""
    Based on 2019-2025 trend analysis:

    ✅ HIGH PRIORITY (consistently important):
       1. Engineering Mathematics - Discrete Math, Linear Algebra
       2. Data Structures - Trees, Heaps, Graphs
       3. Operating Systems - Memory Management, Synchronization
       4. Computer Networks - IP Addressing, TCP/UDP

    ⬆️ RISING IMPORTANCE:
       1. Computer Organization - Up from 8 to 12 marks (2019→2025)
       2. Programming - Variable but trending up in 2025
       3. Digital Logic - Spiked to 8 marks in 2023

    ⬇️ DECLINING (but still important):
       1. Theory of Computation - Down from 11 to 7 marks
       2. Engineering Math - Slightly down from 15 to 12

    💡 FOCUS AREAS FOR 2026:
       • Memory Hierarchy & Cache (COA) - 4 marks avg
       • Data Structures (Trees, Heaps) - 4 marks avg
       • Graph Algorithms (MST, Shortest Path) - 3 marks avg
       • Parsing (LR, SLR) - 3 marks avg
       • IP Addressing & Routing - 3 marks avg
    """)


def main():
    print("\n" + "=" * 70)
    print("GATE EXTERNAL DATA ANALYSIS")
    print("=" * 70)
    
    # 1. Analyze external data
    external_avgs = analyze_external_data()
    
    # 2. Load and analyze our data
    our_data = load_our_data()
    
    # 3. Compare datasets
    compare_datasets(external_avgs, our_data)
    
    # 4. Generate recommendations
    generate_recommendations()
    
    # 5. Save analysis to JSON
    analysis_output = {
        "source": "Biraj2004/GATE_CS-2026_Analysis",
        "years_covered": EXTERNAL_DATA['years'],
        "subject_marks": EXTERNAL_DATA['marks'],
        "topic_weightage": EXTERNAL_DATA['topicwise'],
        "insights": {
            "rising_subjects": ["Computer Organization & Architecture", "Programming & Data Structures"],
            "falling_subjects": ["Theory of Computation", "Engineering & Discrete Mathematics"],
            "top_topics": [
                {"topic": "Discrete Maths", "subject": "Engineering Mathematics", "marks": 8},
                {"topic": "Memory Hierarchy & Cache", "subject": "Computer Organization", "marks": 4},
                {"topic": "Data Structures (Trees, Heaps)", "subject": "Data Structures", "marks": 4},
                {"topic": "Graph Algorithms", "subject": "Algorithms", "marks": 3},
                {"topic": "Parsing (LR, SLR)", "subject": "Compiler Design", "marks": 3}
            ]
        }
    }
    
    with open("external_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis_output, f, indent=2)
    
    print("\n✅ Analysis saved to: external_analysis.json")


if __name__ == "__main__":
    main()
