import json
import os
import tempfile
from datetime import datetime, timezone

Q_PATH = "Q.json"
TAX_PATH = "golden_taxonomy.json"
CHECKPOINT_PATH = "audit_checkpoint.json"
REPORT_PATH = "delta_report_full.json"

def atomic_json_write(path, value):
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(prefix=".audit_", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_checkpoint(checkpoint):
    checkpoint["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_json_write(CHECKPOINT_PATH, checkpoint)
    atomic_json_write(REPORT_PATH, checkpoint["results"])

def get_subject_taxonomy(taxonomy, subject):
    return taxonomy.get(subject, {})

def format_taxonomy_for_prompt(taxonomy):
    lines = []
    for concept, data in taxonomy.items():
        lines.append(f"Concept: {concept}")
        for mt in data.get("micro_topics", []):
            lines.append(f"  - {mt}")
    return "\n".join(lines)

def audit_question(q, subject_taxonomy, index):
    subject = q.get("subject", "")
    question_text = q.get("question_text", "")
    choices = q.get("choices", {})
    old_concept = q.get("topic", "")
    old_micro = q.get("micro_topic", "")

    taxonomy_str = format_taxonomy_for_prompt(subject_taxonomy)

    prompt = f"""You are a GATE CS examiner. Map this question to the Golden Taxonomy.

Subject: {subject}
Question: {question_text}
Choices: {json.dumps(choices, ensure_ascii=False)}

Golden Taxonomy for this subject:
{taxonomy_str}

Current (possibly wrong) label:
- Concept: {old_concept}
- Micro-topic: {old_micro}

Return JSON only: {{"concept": "...", "micro_topic": "...", "reasoning": "..."}}
Only use concepts/micro-topics from the taxonomy. If none fit exactly, propose a precise new micro-topic under the correct concept."""

    return prompt

def process_batch(start_index, batch_size=50):
    questions = load_json(Q_PATH)
    taxonomy = load_json(TAX_PATH)

    if os.path.exists(CHECKPOINT_PATH):
        checkpoint = load_json(CHECKPOINT_PATH)
    else:
        checkpoint = {
            "version": 1,
            "source": Q_PATH,
            "total_questions": len(questions),
            "last_processed_index": -1,
            "completed": 0,
            "status": "processing",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "results": []
        }

    last_index = checkpoint.get("last_processed_index", -1)
    if start_index <= last_index:
        start_index = last_index + 1

    end_index = min(start_index + batch_size, len(questions))

    print(f"Processing questions {start_index} to {end_index - 1} (inclusive)")
    print(f"Total questions: {len(questions)}")

    batch_results = []

    for i in range(start_index, end_index):
        q = questions[i]
        subject = q.get("subject", "")
        subject_taxonomy = get_subject_taxonomy(taxonomy, subject)

        if not subject_taxonomy:
            # No taxonomy for this subject, keep original
            result = {
                "index": i,
                "question_number": q.get("question_number"),
                "year": q.get("year"),
                "subject": subject,
                "question_text_preview": q.get("question_text", "")[:150],
                "old_concept": q.get("topic", ""),
                "old_micro": q.get("micro_topic", ""),
                "new_concept": q.get("topic", ""),
                "new_micro": q.get("micro_topic", ""),
                "reasoning": "No taxonomy available for subject",
                "changed": False
            }
        else:
            # For now, we'll mark as needing manual review
            # In actual run, this would call an LLM
            result = {
                "index": i,
                "question_number": q.get("question_number"),
                "year": q.get("year"),
                "subject": subject,
                "question_text_preview": q.get("question_text", "")[:150],
                "old_concept": q.get("topic", ""),
                "old_micro": q.get("micro_topic", ""),
                "new_concept": "",
                "new_micro": "",
                "reasoning": "PENDING_LLM_REVIEW",
                "changed": None
            }

        batch_results.append(result)
        checkpoint["results"].append(result)
        checkpoint["last_processed_index"] = i
        checkpoint["completed"] = i + 1

        # Save checkpoint every question
        if i % 10 == 0 or i == end_index - 1:
            save_checkpoint(checkpoint)

    checkpoint["status"] = "processing" if end_index < len(questions) else "completed"
    save_checkpoint(checkpoint)

    print(f"Batch complete. Checkpoint saved. Last index: {checkpoint['last_processed_index']}")
    return batch_results

if __name__ == "__main__":
    import sys
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    process_batch(start, batch_size)