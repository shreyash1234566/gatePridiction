"""Resumable semantic-audit queue for Q.json.

This script never changes Q.json. It creates/updates audit_checkpoint.json and
an audit queue so question-level decisions can be supplied and validated safely.
"""
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


def build_checkpoint(questions):
    now = datetime.now(timezone.utc).isoformat()
    return {
        "version": 1,
        "source": Q_PATH,
        "total_questions": len(questions),
        "last_processed_index": -1,
        "completed": 0,
        "status": "initialized",
        "updated_at": now,
        "results": [],
    }


def main():
    questions = load_json(Q_PATH)
    taxonomy = load_json(TAX_PATH)

    if os.path.exists(CHECKPOINT_PATH):
        checkpoint = load_json(CHECKPOINT_PATH)
        if checkpoint.get("total_questions") != len(questions):
            raise RuntimeError("Q.json length changed; refusing to resume mismatched checkpoint")
    else:
        checkpoint = build_checkpoint(questions)
        atomic_json_write(CHECKPOINT_PATH, checkpoint)

    # Materialize a review queue without making semantic claims. Each entry is
    # pending until a human/LLM examiner supplies a validated mapping.
    queue = []
    for index, q in enumerate(questions):
        if index <= checkpoint.get("last_processed_index", -1):
            continue
        subject = q.get("subject", "")
        queue.append({
            "index": index,
            "question_number": q.get("question_number"),
            "year": q.get("year"),
            "subject": subject,
            "old_topic": q.get("topic", ""),
            "old_micro_topic": q.get("micro_topic", ""),
            "question_text": q.get("question_text", ""),
            "choices": q.get("choices", {}),
            "allowed_taxonomy": taxonomy.get(subject, {}),
            "status": "pending",
        })

    atomic_json_write("audit_queue.json", queue)
    checkpoint["status"] = "queued"
    checkpoint["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_json_write(CHECKPOINT_PATH, checkpoint)
    atomic_json_write(REPORT_PATH, checkpoint["results"])

    print(f"Q.json questions: {len(questions)}")
    print(f"Checkpoint completed: {checkpoint['completed']}")
    print(f"Pending semantic reviews: {len(queue)}")
    print(f"Checkpoint: {CHECKPOINT_PATH}")
    print(f"Queue: { 'audit_queue.json' }")
    print("No production file was modified.")


if __name__ == "__main__":
    main()
