"""
Compare Kaggle GATE dataset with our Q.json
============================================
Find unique questions and potential additions
"""

import pandas as pd
import json
from difflib import SequenceMatcher
from collections import Counter

# Load Kaggle data
kaggle_df = pd.read_csv('kaggle_data/questions-data/questions-data-new.csv')
print(f"📦 Kaggle Dataset: {len(kaggle_df)} questions")

# Load our Q.json
with open('Q.json', 'r', encoding='utf-8') as f:
    our_data = json.load(f)
print(f"📦 Our Q.json: {len(our_data)} questions")

# Extract question text from our data
our_questions = set()
for q in our_data:
    question_text = q.get('question', '').strip().lower()[:100]  # First 100 chars
    if question_text:
        our_questions.add(question_text)

print(f"\n🔍 Unique question starts in our data: {len(our_questions)}")

# Check for matches
def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Find potentially new questions
new_questions = []
duplicates = []

print("\n⏳ Analyzing questions (this may take a moment)...")

for idx, row in kaggle_df.iterrows():
    kaggle_q = row['question'][:100].lower()
    topic = row['topic']
    
    # Check if similar question exists
    is_duplicate = False
    for our_q in our_questions:
        if similarity(kaggle_q, our_q) > 0.7:
            is_duplicate = True
            break
    
    if is_duplicate:
        duplicates.append(row)
    else:
        new_questions.append({
            'topic': topic,
            'question': row['question']
        })

print("\n" + "=" * 60)
print("📊 COMPARISON RESULTS")
print("=" * 60)
print(f"✅ Potentially NEW questions: {len(new_questions)}")
print(f"🔄 Duplicates/Similar: {len(duplicates)}")

# Topic breakdown of new questions
print("\n📈 NEW Questions by Topic:")
print("-" * 40)
new_by_topic = Counter(q['topic'] for q in new_questions)
for topic, count in sorted(new_by_topic.items(), key=lambda x: -x[1]):
    print(f"  {topic:<45s}: {count:4d}")

# Show sample new questions
print("\n📝 Sample NEW Questions (first 3 per topic):")
print("-" * 60)
shown = Counter()
for q in new_questions[:50]:
    topic = q['topic']
    if shown[topic] < 2:
        print(f"\n[{topic}]")
        print(f"  {q['question'][:150]}...")
        shown[topic] += 1

# Save new questions to file
with open('kaggle_new_questions.json', 'w', encoding='utf-8') as f:
    json.dump(new_questions, f, indent=2, ensure_ascii=False)

print(f"\n💾 Saved {len(new_questions)} new questions to: kaggle_new_questions.json")

# Summary
print("\n" + "=" * 60)
print("📋 SUMMARY")
print("=" * 60)
print(f"""
Kaggle Dataset:     {len(kaggle_df):,} questions
Our Q.json:         {len(our_data):,} questions
Potentially New:    {len(new_questions):,} questions
Overlap/Similar:    {len(duplicates):,} questions

🎯 You could potentially add {len(new_questions)} NEW questions!

Note: The Kaggle dataset has ONLY topic & question text.
      Missing: year, marks, options, correct answer
      
⚠️ To merge: Would need to manually add year/marks/answers
""")
