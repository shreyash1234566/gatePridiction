"""
Generate comprehensive data.js for GATE 2027 Website
=====================================================
Combines:
1. All PYQs from Q.json (topic-wise, year-wise)
2. Predictions from elite_predictions_2027.json
3. Trend analysis per topic
4. Subject distribution
5. Mock paper generation data
"""

import json
from collections import defaultdict
from datetime import datetime

# Subject distribution (must match prediction system)
SECTION_DISTRIBUTION = {
    "Engineering Mathematics": 9,
    "Digital Logic": 3,
    "Computer Organization": 6,
    "Programming": 2,
    "Data Structures": 7,
    "Algorithms": 4,
    "Theory of Computation": 5,
    "Compiler Design": 3,
    "Operating Systems": 6,
    "Databases": 4,
    "Computer Networks": 5,
    "General Aptitude": 11
}

# Subject normalization (same as prediction system)
SUBJECT_MAPPING = {
    "engineering mathematics": "Engineering Mathematics",
    "engg mathematics": "Engineering Mathematics",
    "discrete mathematics": "Engineering Mathematics",
    "linear algebra": "Engineering Mathematics",
    "probability and statistics": "Engineering Mathematics",
    "probability": "Engineering Mathematics",
    "mathematics": "Engineering Mathematics",
    "digital logic": "Digital Logic",
    "digital electronics": "Digital Logic",
    "boolean algebra": "Digital Logic",
    "computer organization and architecture": "Computer Organization",
    "computer organization & architecture": "Computer Organization",
    "computer architecture": "Computer Organization",
    "computer organization": "Computer Organization",
    "coa": "Computer Organization",
    "programming and data structures": "Programming",
    "programming & data structures": "Programming",
    "programming in c": "Programming",
    "c programming": "Programming",
    "programming": "Programming",
    "data structures": "Data Structures",
    "data structure": "Data Structures",
    "algorithms": "Algorithms",
    "algorithm": "Algorithms",
    "design and analysis of algorithms": "Algorithms",
    "theory of computation": "Theory of Computation",
    "formal languages and automata theory": "Theory of Computation",
    "automata theory": "Theory of Computation",
    "compiler design": "Compiler Design",
    "compilers": "Compiler Design",
    "operating systems": "Operating Systems",
    "operating system": "Operating Systems",
    "databases": "Databases",
    "database": "Databases",
    "database management systems": "Databases",
    "dbms": "Databases",
    "computer networks": "Computer Networks",
    "networking": "Computer Networks",
    "networks": "Computer Networks",
    "general aptitude": "General Aptitude",
    "aptitude": "General Aptitude",
    "verbal ability": "General Aptitude",
    "numerical ability": "General Aptitude"
}

# Invalid subjects to skip
INVALID_SUBJECTS = {"Software Engineering", "Web Technologies", "Web Technology", 
                    "Artificial Intelligence", "Machine Learning"}

def normalize_subject(subject_raw):
    """Normalize subject name to standard form."""
    if not subject_raw:
        return None
    subject = str(subject_raw).strip().lower()
    
    # Check invalid subjects
    for invalid in INVALID_SUBJECTS:
        if invalid.lower() == subject:
            return None
    
    # Direct mapping
    if subject in SUBJECT_MAPPING:
        return SUBJECT_MAPPING[subject]
    
    # Substring matching
    for key, val in SUBJECT_MAPPING.items():
        if key in subject or subject in key:
            return val
    
    # Check if already valid
    if subject_raw in SECTION_DISTRIBUTION:
        return subject_raw
    
    return None

def load_questions(file_path="Q.json"):
    """Load and process questions from Q.json."""
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    processed = []
    for q in questions:
        raw_subject = q.get('subject') or q.get('section')
        subject = normalize_subject(raw_subject)
        
        if subject is None:
            continue
        
        year = q.get('year')
        if not year:
            continue
        
        processed.append({
            'id': len(processed) + 1,
            'year': int(year),
            'paper_id': q.get('paper_id', ''),
            'subject': subject,
            'topic': q.get('topic') or q.get('topic_name') or subject,
            'micro_topic': q.get('micro_topic') or q.get('topic') or q.get('topic_name') or subject,
            'question_text': q.get('question_text') or q.get('question') or q.get('text') or '',
            'question_type': q.get('question_type', 'MCQ'),
            'choices': q.get('choices', []),
            'answer': q.get('answer', ''),
            'marks': q.get('marks', 1),
            'negative_marks': q.get('negative_marks', 0.33)
        })
    
    return processed

def load_predictions(file_path="elite_predictions_2027.json"):
    """Load predictions from elite_predictions_2027.json."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_trends(questions):
    """Calculate trend data for each topic."""
    # Group by subject and topic
    topic_data = defaultdict(lambda: {
        'years': [],
        'counts': defaultdict(int),
        'questions': []
    })
    
    for q in questions:
        key = f"{q['subject']}|{q['topic']}"
        topic_data[key]['years'].append(q['year'])
        topic_data[key]['counts'][q['year']] += 1
        topic_data[key]['questions'].append(q['id'])
    
    trends = {}
    for key, data in topic_data.items():
        subject, topic = key.split('|', 1)
        unique_years = sorted(set(data['years']))
        
        if len(unique_years) == 0:
            continue
        
        year_counts = {y: data['counts'][y] for y in unique_years}
        
        # Calculate trend direction
        if len(unique_years) >= 3:
            recent = sum(data['counts'][y] for y in unique_years[-3:]) / 3
            older = sum(data['counts'][y] for y in unique_years[:-3]) / max(1, len(unique_years) - 3)
            if recent > older * 1.3:
                trend_direction = "Rising"
            elif recent < older * 0.7:
                trend_direction = "Declining"
            else:
                trend_direction = "Stable"
        else:
            trend_direction = "Stable"
        
        trends[key] = {
            'subject': subject,
            'topic': topic,
            'total_appearances': len(data['years']),
            'unique_years': unique_years,
            'year_counts': year_counts,
            'first_seen': min(unique_years),
            'last_seen': max(unique_years),
            'avg_per_year': round(len(data['years']) / len(unique_years), 2),
            'trend_direction': trend_direction,
            'question_ids': data['questions']
        }
    
    return trends

def calculate_micro_topic_trends(questions):
    """Calculate trend data for each micro_topic."""
    micro_data = defaultdict(lambda: {
        'years': [],
        'counts': defaultdict(int),
        'questions': []
    })
    
    for q in questions:
        key = f"{q['subject']}|{q['topic']}|{q['micro_topic']}"
        micro_data[key]['years'].append(q['year'])
        micro_data[key]['counts'][q['year']] += 1
        micro_data[key]['questions'].append(q['id'])
    
    trends = {}
    for key, data in micro_data.items():
        parts = key.split('|', 2)
        if len(parts) < 3:
            continue
        subject, topic, micro_topic = parts
        unique_years = sorted(set(data['years']))
        
        if len(unique_years) == 0:
            continue
        
        year_counts = {y: data['counts'][y] for y in unique_years}
        
        if len(unique_years) >= 3:
            recent = sum(data['counts'][y] for y in unique_years[-3:]) / 3
            older = sum(data['counts'][y] for y in unique_years[:-3]) / max(1, len(unique_years) - 3)
            if recent > older * 1.3:
                trend_direction = "Rising"
            elif recent < older * 0.7:
                trend_direction = "Declining"
            else:
                trend_direction = "Stable"
        else:
            trend_direction = "Stable"
        
        trends[key] = {
            'subject': subject,
            'topic': topic,
            'micro_topic': micro_topic,
            'total_appearances': len(data['years']),
            'unique_years': unique_years,
            'year_counts': year_counts,
            'first_seen': min(unique_years),
            'last_seen': max(unique_years),
            'avg_per_year': round(len(data['years']) / len(unique_years), 2),
            'trend_direction': trend_direction,
            'question_ids': data['questions']
        }
    
    return trends

def organize_by_subject(questions):
    """Organize questions by subject."""
    by_subject = defaultdict(list)
    for q in questions:
        by_subject[q['subject']].append(q)
    return dict(by_subject)

def organize_by_year(questions):
    """Organize questions by year."""
    by_year = defaultdict(list)
    for q in questions:
        by_year[q['year']].append(q)
    return {str(k): v for k, v in sorted(by_year.items())}

def organize_by_topic(questions):
    """Organize questions by subject > topic."""
    by_topic = defaultdict(lambda: defaultdict(list))
    for q in questions:
        by_topic[q['subject']][q['topic']].append(q)
    
    return {subj: dict(topics) for subj, topics in by_topic.items()}

def generate_year_stats(questions):
    """Generate statistics for each year."""
    by_year = defaultdict(lambda: {
        'total': 0,
        'subjects': defaultdict(int),
        'types': defaultdict(int),
        'papers': set()
    })
    
    for q in questions:
        year = q['year']
        by_year[year]['total'] += 1
        by_year[year]['subjects'][q['subject']] += 1
        by_year[year]['types'][q['question_type']] += 1
        by_year[year]['papers'].add(q['paper_id'])
    
    stats = {}
    for year, data in sorted(by_year.items()):
        stats[str(year)] = {
            'total_questions': data['total'],
            'num_papers': len(data['papers']),
            'papers': list(data['papers']),
            'subject_distribution': dict(data['subjects']),
            'question_types': dict(data['types'])
        }
    
    return stats

def generate_subject_stats(questions):
    """Generate statistics for each subject."""
    by_subject = defaultdict(lambda: {
        'total': 0,
        'topics': defaultdict(int),
        'years': defaultdict(int)
    })
    
    for q in questions:
        subj = q['subject']
        by_subject[subj]['total'] += 1
        by_subject[subj]['topics'][q['topic']] += 1
        by_subject[subj]['years'][q['year']] += 1
    
    stats = {}
    for subj, data in by_subject.items():
        hot_topics = sorted(data['topics'].items(), key=lambda x: -x[1])[:10]
        stats[subj] = {
            'total_questions': data['total'],
            'expected_2027': SECTION_DISTRIBUTION.get(subj, 0),
            'num_topics': len(data['topics']),
            'hot_topics': [{'topic': t, 'count': c} for t, c in hot_topics],
            'year_distribution': {str(y): c for y, c in sorted(data['years'].items())}
        }
    
    return stats

def generate_mock_paper_config(predictions_data, questions):
    """Generate mock paper configuration based on predictions."""
    predictions = predictions_data.get('predictions', [])
    
    # Group predictions by subject
    by_subject = defaultdict(list)
    for p in predictions:
        by_subject[p['subject']].append({
            'topic': p['topic'],
            'weight': p['predicted_count'],
            'confidence': p['confidence'],
            'trend': p.get('trend', 'Stable')
        })
    
    # Find available questions for each topic
    topic_questions = defaultdict(list)
    for q in questions:
        key = f"{q['subject']}|{q['topic']}"
        topic_questions[key].append(q['id'])
    
    mock_config = {
        'total_questions': 65,
        'total_marks': 100,
        'duration_minutes': 180,
        'subject_quotas': SECTION_DISTRIBUTION,
        'topic_weights': {},
        'difficulty_mix': {
            '1_mark': 25,
            '2_mark': 40
        }
    }
    
    for subj, topics in by_subject.items():
        mock_config['topic_weights'][subj] = []
        for t in sorted(topics, key=lambda x: -x['weight']):
            key = f"{subj}|{t['topic']}"
            mock_config['topic_weights'][subj].append({
                'topic': t['topic'],
                'weight': round(t['weight'], 3),
                'confidence': t['confidence'],
                'available_questions': len(topic_questions.get(key, []))
            })
    
    return mock_config

def main():
    print("📊 Generating comprehensive data.js for GATE 2027 Website...")
    
    # Load data
    print("   Loading Q.json...")
    questions = load_questions("Q.json")
    print(f"   ✓ Loaded {len(questions)} valid questions")
    
    print("   Loading predictions...")
    predictions_data = load_predictions("elite_predictions_2027.json")
    print(f"   ✓ Loaded {len(predictions_data.get('predictions', []))} predictions")
    
    # Calculate trends
    print("   Calculating trends...")
    trends = calculate_trends(questions)
    print(f"   ✓ Analyzed {len(trends)} topic trends")
    
    # Calculate micro_topic trends
    print("   Calculating micro-topic trends...")
    micro_trends = calculate_micro_topic_trends(questions)
    print(f"   ✓ Analyzed {len(micro_trends)} micro-topic trends")
    
    # Generate statistics
    print("   Generating statistics...")
    year_stats = generate_year_stats(questions)
    subject_stats = generate_subject_stats(questions)
    
    # Generate mock paper config
    print("   Generating mock paper configuration...")
    mock_config = generate_mock_paper_config(predictions_data, questions)
    
    # Organize questions
    print("   Organizing questions...")
    questions_by_subject = organize_by_subject(questions)
    questions_by_year = organize_by_year(questions)
    questions_by_topic = organize_by_topic(questions)
    
    # Build final data structure
    data = {
        'meta': {
            'generated_at': datetime.now().isoformat(),
            'version': '5.0 - Complete Website Data with Micro-Topics',
            'description': 'Comprehensive GATE CS data for PYQ practice, trend analysis, predictions (topic + micro-topic), and mock tests',
            'total_questions': len(questions),
            'years_covered': list(sorted(set(q['year'] for q in questions))),
            'subjects': list(SECTION_DISTRIBUTION.keys()),
            'target_year': 2027
        },
        
        'predictions_2027': {
            'meta': predictions_data.get('meta', {}),
            'subject_distribution': SECTION_DISTRIBUTION,
            'predictions': predictions_data.get('predictions', []),
            'micro_topic_predictions': predictions_data.get('micro_topic_predictions', []),
            'subject_totals': predictions_data.get('subject_totals', {}),
            'validation': predictions_data.get('validation', {})
        },
        
        'trends': {
            'by_topic': list(trends.values()),
            'by_micro_topic': list(micro_trends.values()),
            'hot_topics': sorted(
                [t for t in trends.values() if t['last_seen'] >= 2023],
                key=lambda x: (-x['total_appearances'], -x['last_seen'])
            )[:50],
            'rising_topics': [t for t in trends.values() if t['trend_direction'] == 'Rising'],
            'declining_topics': [t for t in trends.values() if t['trend_direction'] == 'Declining']
        },
        
        'statistics': {
            'by_year': year_stats,
            'by_subject': subject_stats
        },
        
        'mock_paper': mock_config,
        
        'questions': {
            'all': questions,
            'by_subject': questions_by_subject,
            'by_year': questions_by_year,
            'by_topic': questions_by_topic
        }
    }
    
    # Write to data.js
    print("   Writing data.js...")
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write('// GATE 2027 Comprehensive Website Data\n')
        f.write('// Auto-generated on ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
        f.write('// Contains: PYQs, Predictions (Topic + Micro-Topic), Trends, Statistics, Mock Paper Config\n\n')
        
        f.write('const GATE_DATA = ')
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write(';\n\n')
        
        # Add helper exports for different use cases
        f.write('// Quick access exports\n')
        f.write('const predictions2027 = GATE_DATA.predictions_2027;\n')
        f.write('const microTopicPredictions = GATE_DATA.predictions_2027.micro_topic_predictions;\n')
        f.write('const allQuestions = GATE_DATA.questions.all;\n')
        f.write('const questionsBySubject = GATE_DATA.questions.by_subject;\n')
        f.write('const questionsByYear = GATE_DATA.questions.by_year;\n')
        f.write('const questionsByTopic = GATE_DATA.questions.by_topic;\n')
        f.write('const trends = GATE_DATA.trends;\n')
        f.write('const microTopicTrends = GATE_DATA.trends.by_micro_topic;\n')
        f.write('const statistics = GATE_DATA.statistics;\n')
        f.write('const mockPaperConfig = GATE_DATA.mock_paper;\n\n')
        
        f.write('// Export for Node.js/ES modules\n')
        f.write('if (typeof module !== "undefined" && module.exports) {\n')
        f.write('  module.exports = { GATE_DATA, predictions2027, microTopicPredictions, allQuestions, questionsBySubject, questionsByYear, questionsByTopic, trends, microTopicTrends, statistics, mockPaperConfig };\n')
        f.write('}\n')
    
    print(f"\n✅ Successfully generated data.js")
    print(f"   📊 Total Questions: {len(questions)}")
    print(f"   📈 Topic Trends: {len(trends)}")
    print(f"   🎯 2027 Predictions: {len(predictions_data.get('predictions', []))}")
    print(f"   📝 Subjects: {len(SECTION_DISTRIBUTION)}")
    print(f"   📅 Years: {min(q['year'] for q in questions)} - {max(q['year'] for q in questions)}")

if __name__ == "__main__":
    main()
