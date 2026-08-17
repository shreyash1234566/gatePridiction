# AGENT GUIDE — Full Semantic GATE Question Taxonomy Audit

## 0. Mission and current instruction

You are an autonomous LLM/software agent taking over the semantic classification task for the GATE Computer Science question bank.

**Do not assume that the existing labels are correct.** The purpose of this task is to read the question text and choices, determine what the question actually tests, and assign a consistent three-layer label:

```text
Subject -> Topic/Concept -> Micro-topic
```

The final production dataset must be a reliable, auditable training corpus. Every question must be covered, every accepted label must be a legal path in the canonical taxonomy, and uncertain or incomplete cases must be explicitly abstained rather than guessed.

The user explicitly requested that the work be stopped and handed to another agent with a complete guide. Do not continue any previous partial audit merely because files exist. First inspect the current state, verify hashes/counts, and then follow this guide.

A literal mathematical proof that every automatically generated semantic label is correct is impossible without independently verified gold labels and complete question evidence. The correct engineering objective is:

> Accept a label only when all deterministic and evidence-based acceptance conditions pass; otherwise send the record to `manual_review`, `blocked`, or `input_defect`. Establish the accepted-set error rate on an independently reviewed gold set before claiming performance.

Do not fabricate a 100% accuracy claim. A 100% **coverage** run is required; 100% **correctness** can only be claimed for a specifically verified accepted set under a declared validation protocol.

---

## 1. Repository and exact file locations

The working repository is:

```text
E:\GATE PRIDICTION
```

Equivalent forward-slash paths that are convenient in Python/Git Bash are:

```text
E:/GATE PRIDICTION
```

Use absolute paths when invoking scripts from outside the repository. All paths below are relative to this repository unless an absolute path is shown.

### 1.1 Primary source and taxonomy files

| File | Exact location | Role | Production status |
|---|---|---|---|
| `Q.json` | `E:/GATE PRIDICTION/Q.json` | Current source question array; 1,621 records, years 2011–2026 | **Read-only source during audit** |
| `Q_original_backup.json` | `E:/GATE PRIDICTION/Q_original_backup.json` | Earlier backup of the source dataset | Preserve; verify its contents/hash before relying on it |
| `Q_full_pre_audit_backup.json` | `E:/GATE PRIDICTION/Q_full_pre_audit_backup.json` | Backup made before an earlier audit attempt | Preserve; compare hashes/counts |
| `Q_unified.json` | `E:/GATE PRIDICTION/Q_unified.json` | Earlier structural migration output | **Not automatically production truth**; inspect before use |
| `golden_taxonomy.json` | `E:/GATE PRIDICTION/golden_taxonomy.json` | Current nested three-layer canonical taxonomy: Subject -> Topic/Concept -> `micro_topics[]` | Canonical label source for the current task |
| `gate_syllabus.json` | `E:/GATE PRIDICTION/gate_syllabus.json` | Generated GATE syllabus vocabulary, broader than the reduced golden taxonomy in places | Syllabus evidence/reference; compare against golden taxonomy |
| `canonical_taxonomy.json` | `E:/GATE PRIDICTION/canonical_taxonomy.json` | Flattened dictionary keyed by strings such as `Algorithms::...` | Historical canonical mapping source; not a nested tree |
| `canonical_taxonomy_pre_audit_backup.json` | `E:/GATE PRIDICTION/canonical_taxonomy_pre_audit_backup.json` | Backup of the flattened canonical mapping | Historical reference only |

### 1.2 Audit and report files

| File | Exact location | Role | Current known state |
|---|---|---|---|
| `audit_engine.py` | `E:/GATE PRIDICTION/audit_engine.py` | Resumable queue/checkpoint initializer | Creates a queue but does not semantically classify questions |
| `audit_checkpoint.json` | `E:/GATE PRIDICTION/audit_checkpoint.json` | Progress and result checkpoint | At handoff: initialized/queued, `completed = 0`, `last_processed_index = -1` |
| `audit_queue.json` | `E:/GATE PRIDICTION/audit_queue.json` | Materialized pending review queue | Contains all 1,621 pending records at handoff |
| `delta_report_full.json` | `E:/GATE PRIDICTION/delta_report_full.json` | Intended old-to-new change report | Empty/no semantic decisions at handoff |
| `full_audit_report.json` | `E:/GATE PRIDICTION/full_audit_report.json` | Heuristic TF-IDF mismatch report | Triage only; never treat as authoritative classification |
| `run_audit_batch.py` | `E:/GATE PRIDICTION/run_audit_batch.py` | Incomplete placeholder batch/checkpoint script | It writes `PENDING_LLM_REVIEW`; it does **not** perform semantic LLM review |
| `batch_0_49.json` | `E:/GATE PRIDICTION/batch_0_49.json` | First 50-question inspection extract | Reference extract only; not a final result |
| `Q_2026_audit_input.json` | `E:/GATE PRIDICTION/Q_2026_audit_input.json` | Earlier 2026-only audit input | Only 2026; must not be confused with the full dataset |
| `audit_args.json` | `E:/GATE PRIDICTION/audit_args.json` | Arguments for an earlier generated workflow | Historical 2026 workflow input |
| `audit_args_fixed.json` | `E:/GATE PRIDICTION/audit_args_fixed.json` | Corrected historical workflow arguments | Historical reference |
| `audit_2026_workflow.js` | `E:/GATE PRIDICTION/audit_2026_workflow.js` | Earlier 2026-only workflow | Not sufficient for the all-years task |
| `audit_2026_compiled.js` | `E:/GATE PRIDICTION/audit_2026_compiled.js` | Generated 2026-only JavaScript audit | Not sufficient for the all-years task |
| `prepare_audit.py` | `E:/GATE PRIDICTION/prepare_audit.py` | Earlier audit preparation helper | Inspect before reuse |
| `prepare_audit_args.py` | `E:/GATE PRIDICTION/prepare_audit_args.py` | Earlier workflow argument helper | Historical helper |
| `ml_nlp_audit.py` | `E:/GATE PRIDICTION/ml_nlp_audit.py` | TF-IDF similarity triage | Not a semantic ground-truth classifier |

### 1.3 Taxonomy-generation and migration scripts

| File | Location | Role |
|---|---|---|
| `build_golden_taxonomy.py` | `E:/GATE PRIDICTION/build_golden_taxonomy.py` | Builds nested golden taxonomy from `canonical_taxonomy_pre_audit_backup.json` |
| `build_golden_taxonomy_prep.py` | `E:/GATE PRIDICTION/build_golden_taxonomy_prep.py` | Analyzes canonical mappings and unmapped labels |
| `map_unified.py` | `E:/GATE PRIDICTION/map_unified.py` | Attempts to map existing micro-topics to concepts using reverse lookup |
| `build_taxonomy.py` | `E:/GATE PRIDICTION/build_taxonomy.py` | Earlier taxonomy construction helper |
| `fix_taxonomy.py` | `E:/GATE PRIDICTION/fix_taxonomy.py` | Earlier taxonomy repair helper |
| `fix_taxonomy_final.py` | `E:/GATE PRIDICTION/fix_taxonomy_final.py` | Later taxonomy repair helper |
| `make_syllabus.py` | `E:/GATE PRIDICTION/make_syllabus.py` | Earlier syllabus generation helper |
| `make_syllabus_fixed.py` | `E:/GATE PRIDICTION/make_syllabus_fixed.py` | Corrected syllabus-generation helper |

Do not run taxonomy-generation or migration scripts blindly against production files. First copy outputs to a versioned sandbox and compare counts, paths, and hashes.

### 1.4 Other project files

The repository also contains the application under:

```text
E:/GATE PRIDICTION/focus-flow
E:/GATE PRIDICTION/src
```

There are copies of question data at:

```text
E:/GATE PRIDICTION/src/data/Q.json
E:/GATE PRIDICTION/focus-flow/src/data/Q.json
```

These application copies are not automatically the audit source. The source explicitly under audit is the root file:

```text
E:/GATE PRIDICTION/Q.json
```

Do not update application copies until the audited root dataset is approved and a separate synchronization decision is made.

---

## 2. Dataset contract and three-layer terminology

The target hierarchy is exactly three semantic layers:

```text
Subject -> Topic (also called Concept in some earlier notes) -> Micro-topic
```

Use one field name consistently in the output. The existing raw data uses `topic`; the current golden taxonomy uses dictionary keys for the middle layer and calls the leaves `micro_topics`. For compatibility, the recommended normalized record contains both:

```json
{
  "subject": "Operating Systems",
  "topic": "CPU Scheduling",
  "micro_topic": "Shortest Job First (SJF) Scheduling"
}
```

If a new `concept` alias is added, it must equal `topic`; do not create a fourth semantic layer.

### 2.1 Existing `Q.json` record shape

A normal record looks like:

```json
{
  "year": 2011,
  "file_name": "GATE2011.pdf",
  "paper_id": "GATE_CS_2011",
  "subject": "Compiler Design",
  "topic": "Lexical Analysis",
  "micro_topic": "Keyword and Token Recognition",
  "question_text": "In a compiler, keywords of a language are recognized during",
  "question_type": "MCQ",
  "choices": [
    "(A) parsing of the program",
    "(B) the code generation",
    "(C) the lexical analysis of the program",
    "(D) dataflow analysis"
  ],
  "answer": "(C)",
  "marks": 1,
  "negative_marks": 0.33,
  "is_shared_question": false
}
```

Important details:

- `question_text` is the primary semantic evidence.
- `choices` is an array for MCQs/MSQs and may be absent or empty for NAT questions.
- `answer` must not be treated as the topic label; it can help interpret a question but cannot substitute for missing wording.
- Some records include OCR artifacts, placeholders such as `[Diagram]`, `[Table]`, `[Circuit A]`, or references to an image that is not stored in the JSON.
- Some questions refer to “the previous question,” a “figure below,” or a table. These must be flagged if the required context is unavailable.
- The original `topic` and `micro_topic` are suspicious candidate labels, not verified truth.

### 2.2 Taxonomy shape

`golden_taxonomy.json` is a nested object:

```json
{
  "Subject Name": {
    "Topic Name": {
      "micro_topics": [
        "Micro-topic A",
        "Micro-topic B"
      ]
    }
  }
}
```

Example:

```json
{
  "Operating Systems": {
    "CPU Scheduling": {
      "micro_topics": [
        "Shortest Remaining Time First (SRTF) Scheduling",
        "Shortest Job First (SJF) Scheduling",
        "First Come First Served (FCFS) Scheduling"
      ]
    }
  }
}
```

The legal label path is therefore:

```text
Operating Systems
  -> CPU Scheduling
      -> Shortest Job First (SJF) Scheduling
```

Build a normalized list of legal paths before classification. Each path should have a stable ID, for example:

```text
subject=Operating Systems
 topic=CPU Scheduling
 micro_topic=Shortest Job First (SJF) Scheduling
```

Prefer a deterministic hash of the exact UTF-8 string `subject\n topic\n micro_topic` as `taxonomy_id`.

### 2.3 Historical flattened taxonomy

`canonical_taxonomy.json` is **not** a nested tree. It is keyed like:

```text
Algorithms::Algorithm Design: Dynamic Programming
```

Each value has approximately:

```json
{
  "subject": "Algorithms",
  "topic": "Algorithm Design: Dynamic Programming",
  "canonical_concepts": ["Algorithm Design: Dynamic Programming"],
  "label_to_concept": {
    "Dynamic Programming: Optimal Substructure": "Algorithm Design: Dynamic Programming"
  }
}
```

Correct parser:

```python
for path, entry in canonical_taxonomy.items():
    subject = entry["subject"]
    topic = entry["topic"]
    for micro_topic, mapped_concept in entry.get("label_to_concept", {}).items():
        legal_or_historical_paths.add((subject, topic, micro_topic))
```

Do not parse the flattened key as if it were the entire canonical hierarchy. Do not assume that `canonical_concepts` and `topic` have the same meaning without inspecting the entry.

---

## 3. Syllabus source and taxonomy authority

The GATE syllabus reference generated in this repository is:

```text
E:/GATE PRIDICTION/gate_syllabus.json
```

It contains subject keys and topic keys with arrays of candidate micro-topic terms. It is useful for checking syllabus scope and detecting omissions, but it is not necessarily identical to `golden_taxonomy.json`.

The current project decision is:

1. Use the official/GATE-derived syllabus vocabulary as the scope reference.
2. Use the reviewed nested `golden_taxonomy.json` as the exact legal production taxonomy.
3. If `gate_syllabus.json` contains a syllabus item absent from `golden_taxonomy.json`, do not silently add it during question labeling. Create a taxonomy-gap report and propose a reviewed addition.
4. If `golden_taxonomy.json` contains a label that cannot be justified by the syllabus or a legitimate GATE CS concept, flag it for taxonomy review instead of deleting it automatically.
5. Preserve the three-layer shape. Adding a missing micro-topic is allowed only after evidence and review; inventing arbitrary labels per question is forbidden.

The syllabus may contain broader or alternate names such as `Memory Management`, `Virtual Memory`, `I/O and Disk Scheduling`, or historical aliases. This is not proof that a particular question belongs to that branch. The question text decides the semantic assignment; the taxonomy decides which exact labels are legal.

### 3.1 Taxonomy reconciliation procedure

Before auditing questions:

- Extract every `(subject, topic, micro_topic)` from `golden_taxonomy.json`.
- Extract every `(subject, topic, syllabus_micro_topic)` from `gate_syllabus.json`.
- Normalize only for comparison: Unicode normalization, case folding, whitespace collapse, and reviewed alias mapping. Do not overwrite exact canonical strings.
- Produce:
  - `taxonomy_paths_golden.json`
  - `taxonomy_paths_syllabus_only.json`
  - `taxonomy_paths_golden_only.json`
  - `taxonomy_alias_review_queue.json`
- For each syllabus-only item, decide whether it is:
  - an alias of an existing golden micro-topic,
  - a missing legitimate micro-topic to be reviewed and added,
  - an overly broad/non-GATE item,
  - or a generation artifact.
- Freeze the reconciled taxonomy version and hash it before classifying questions.

The question audit must not use an automatically generated, unreviewed taxonomy as the source of truth.

---

## 4. What happened in earlier attempts and why it was insufficient

### 4.1 2026-only audit confusion

Earlier generated JavaScript workflows (`audit_2026_workflow.js`, `audit_2026_compiled.js`) were designed for approximately 130 questions from 2026 only. They used a schema containing `is_correctly_labeled`, `reasoning`, `suggested_concept`, and `suggested_micro_topic`.

That work must not be reported as an audit of 2011–2026. The required scope is all 1,621 records.

### 4.2 `audit_engine.py` limitation

`audit_engine.py` correctly creates a resumable queue and protects `Q.json`, but it does not call an LLM or make semantic decisions. It only materializes fields such as:

- index
- year
- subject
- old topic
- old micro-topic
- question text
- choices
- allowed taxonomy
- `status: pending`

Its current checkpoint at handoff is:

```json
{
  "total_questions": 1621,
  "last_processed_index": -1,
  "completed": 0,
  "results": [],
  "status": "queued"
}
```

Do not interpret the existence of `audit_queue.json` as completed work.

### 4.3 `run_audit_batch.py` limitation

`run_audit_batch.py` was written as a checkpointing scaffold. For normal taxonomy-covered questions it writes:

```json
{
  "new_concept": "",
  "new_micro": "",
  "reasoning": "PENDING_LLM_REVIEW",
  "changed": null
}
```

It does not perform semantic classification. Do not run it as if it completes the audit. Replace it with a real worker or use a separate implementation that writes valid adjudication results.

### 4.4 TF-IDF limitation

`ml_nlp_audit.py` builds lexical TF-IDF profiles and flags questions whose nearest profile differs from the original label. This is useful for triage only. Similar vocabulary occurs in neighboring topics, and a question may be semantically correct despite low lexical similarity. TF-IDF cannot prove a relabeling.

Never copy its predicted concept directly into production.

### 4.5 Structural lookup limitation

`map_unified.py` reverse-maps micro-topic strings to a concept. This confirms that a label string is present in the taxonomy; it does not confirm that the question text supports that label. Structural membership is necessary but not sufficient.

### 4.6 Resource and workflow failure

Earlier attempts to run large generated multi-agent workflows were unreliable because of workflow/script encoding and resource/capacity limitations. Model rotation cannot create tokens or endpoint capacity. If a model call fails, save the failure as `blocked` and checkpoint immediately. Never convert a service failure into a guessed label or a false semantic mismatch.

### 4.7 Data uniformity warning

The question bank is not uniformly distributed across subjects, years, question types, or micro-topics. Do not assume an i.i.d. random sample is representative. Do not use the existing labels as the evaluation gold set. Use the GATE-derived taxonomy for legal scope and construct a manually verified, stratified calibration/gold set for semantic truth.

The non-uniformity does **not** mean the taxonomy should be ignored. It means evaluation and sampling must account for the distribution and rare labels.

---

## 5. Required end-to-end architecture

Use the following architecture, in order:

```text
Immutable ingestion
  -> taxonomy reconciliation
  -> input-quality/defect detection
  -> deterministic label and keyword evidence
  -> lexical retrieval
  -> dense retrieval (optional but useful)
  -> constrained hierarchical candidates
  -> structured LLM adjudication
  -> independent vote/rerank
  -> deterministic proof checks
  -> calibrated accept/abstain gate
  -> review queue
  -> validated report
  -> atomic production patch only after approval
```

The LLM is an evidence-grounded adjudicator, not an unconstrained label generator. It must select from candidate IDs generated from the legal hierarchy.

### 5.1 Immutable ingestion

Create a run directory, for example:

```text
E:/GATE PRIDICTION/audit_runs/<run_id>/
```

At the start of a run:

- Copy or read `Q.json` without modifying it.
- Hash `Q.json`, `golden_taxonomy.json`, and `gate_syllabus.json` using SHA-256.
- Store hashes in `manifest.json`.
- Validate UTF-8 and JSON structure.
- Record question count, years, subjects, question types, missing fields, duplicate hashes, and invalid taxonomy paths.
- Refuse to continue if a source hash changes during the run.

Recommended manifest:

```json
{
  "source_path": "E:/GATE PRIDICTION/Q.json",
  "taxonomy_path": "E:/GATE PRIDICTION/golden_taxonomy.json",
  "syllabus_path": "E:/GATE PRIDICTION/gate_syllabus.json",
  "source_sha256": "...",
  "taxonomy_sha256": "...",
  "syllabus_sha256": "...",
  "total_questions": 1621,
  "completed_indices": [],
  "failed_indices": [],
  "pipeline_version": "semantic-audit-v1",
  "last_checkpoint_at": "..."
}
```

Preserve both `question_text_raw` and a normalized analysis copy. Do not erase diagrams, tables, code, symbols, or references in the raw copy.

### 5.2 Input defect detection

Set explicit defect flags for:

- missing/empty question text;
- missing choices where choices are required for interpretation;
- `NAT` with no choices (normally valid, not automatically defective);
- `[Diagram]`, `[Circuit]`, `[Network Diagram]`, `[Table]`, “shown below,” “given below,” “as in the previous question,” or similar unresolved references;
- OCR corruption or control characters;
- duplicate or near-duplicate text whose referenced context is not included;
- question text that is too incomplete to distinguish neighboring taxonomy paths.

A record with an essential missing figure/table must not be automatically accepted. It should be `input_defect` or `manual_review`.

### 5.3 Candidate generation

Never prompt an LLM with all 615 micro-topics as unrelated choices. Generate candidates hierarchically:

1. Subject candidates.
2. Topic candidates only under the top one or two subject candidates.
3. Micro-topic candidates only under those topic nodes.
4. Include the original path as a candidate but do not treat it as truth.
5. Include the strongest confusable siblings.
6. Include retrieval-supported candidates.

The final candidate object should contain exact IDs and definitions, for example:

```json
{
  "candidate_id": "tax_abc123",
  "subject": "Operating Systems",
  "topic": "CPU Scheduling",
  "micro_topic": "Shortest Job First (SJF) Scheduling",
  "prototype_text": "Questions about selecting or analyzing shortest-job scheduling...",
  "retrieval_support": ["evidence_17", "evidence_42"]
}
```

The LLM must return `candidate_id`, not a free-form label.

### 5.4 Retrieval evidence

For a 1,621-question corpus, a local hybrid index is sufficient. A vector database is optional, not required.

Use:

- lexical/BM25 search for exact technical terms and named algorithms;
- dense sentence embeddings for paraphrase and semantic similarity;
- optional exact Faiss inner-product search for transparent dense retrieval;
- optional cross-encoder/LLM reranker over only the top few candidates.

Build evidence rows from:

- canonical taxonomy path and prototype text;
- reviewed aliases;
- syllabus definitions;
- independently verified seed examples;
- reviewed confusable examples.

Use multiple question views:

1. Full question plus choices.
2. Question text without choices.
3. Technical-token extraction.
4. A deterministic “what is being computed/tested?” summary if available.

Fuse lexical and dense rankings with reciprocal rank fusion, not by blindly adding incomparable raw scores:

```text
RRF(candidate) = sum over retrievers r of weight_r / (k + rank_r(candidate))
```

For this dataset, exact search is preferred initially because transparency matters more than approximate speed.

### 5.5 Three-level adjudication

The adjudicator must reason in this order:

1. Identify the tested operation/theorem/algorithm/protocol/data structure/language property/mathematical concept.
2. Select the supported Subject.
3. Select the correct Topic under that Subject.
4. Select the most specific correct Micro-topic under that Topic.
5. Reject the strongest confusable sibling explicitly.
6. Detect missing evidence and decide whether to abstain.

Examples of distinctions that must be checked rather than inferred from label strings:

- CPU scheduling versus disk scheduling;
- process context switching versus user/kernel mode switch;
- paging versus virtual-memory page replacement;
- lexical analysis versus syntax analysis;
- Boolean algebra versus logic gates versus combinational circuits;
- graph theory versus graph data-structure representation;
- SQL query semantics versus relational algebra;
- tree properties versus heap properties;
- probability versus random variables versus statistics.

---

## 6. Exact structured adjudication schema and prompt

The following is a starting schema. Improve it by returning candidate IDs and evidence spans. Do not weaken the legal-path validation.

```javascript
const AUDIT_SCHEMA = {
  type: "object",
  properties: {
    is_correctly_labeled: {
      type: "boolean",
      description: "True only if the original Subject/Topic/Micro-topic exactly describe the tested concept at the required granularity. False if wrong, too broad, too narrow, or unsupported."
    },
    tested_concept: {
      type: "string",
      description: "A concise description of what the question actually tests."
    },
    selected_candidate_id: {
      type: "string",
      description: "Exact ID of one candidate path supplied in the prompt. Never invent an ID."
    },
    suggested_subject: {
      type: "string",
      description: "Exact Subject from the selected candidate."
    },
    suggested_topic: {
      type: "string",
      description: "Exact Topic from the selected candidate."
    },
    suggested_micro_topic: {
      type: "string",
      description: "Exact Micro-topic from the selected candidate."
    },
    evidence_spans: {
      type: "array",
      items: { type: "string" },
      description: "Exact phrases, formulas, terms, or choice references supporting the selected path."
    },
    rejected_confusable_candidate_id: {
      type: "string",
      description: "The strongest plausible sibling candidate that was rejected, or empty string if none."
    },
    rejection_reason: {
      type: "string",
      description: "Why the strongest confusable candidate is not correct."
    },
    missing_context: {
      type: "boolean",
      description: "True if a missing diagram, table, previous question, code fragment, or other context prevents reliable classification."
    },
    abstain: {
      type: "boolean",
      description: "True when the evidence is insufficient, candidates are tied, or an input defect prevents a defensible decision."
    },
    reasoning: {
      type: "string",
      description: "Brief evidence-grounded reasoning. Do not rely on label-name similarity alone."
    }
  },
  required: [
    "is_correctly_labeled",
    "tested_concept",
    "selected_candidate_id",
    "suggested_subject",
    "suggested_topic",
    "suggested_micro_topic",
    "evidence_spans",
    "rejected_confusable_candidate_id",
    "rejection_reason",
    "missing_context",
    "abstain",
    "reasoning"
  ],
  additionalProperties: false
};
```

Use this prompt template for each question after candidate generation:

```text
You are a strict GATE Computer Science examiner and taxonomy auditor.

Your job is semantic classification, not answer solving alone. Read the question text and choices carefully. Determine the exact concept being tested, then select one legal three-layer path:
Subject -> Topic -> Micro-topic.

The existing labels are only a hypothesis. They may be wrong and must not be copied without evidence.

QUESTION ID: {question_id}
SOURCE INDEX: {source_index}
YEAR: {year}
QUESTION TYPE: {question_type}

RAW QUESTION TEXT:
{question_text_raw}

CHOICES:
{choices_json_or_EMPTY_FOR_NAT}

ORIGINAL LABEL HYPOTHESIS:
Subject: {original_subject}
Topic: {original_topic}
Micro-topic: {original_micro_topic}

INPUT DEFECT FLAGS:
{defect_flags}

LEGAL CANDIDATE PATHS ONLY:
{candidate_paths_with_ids_and_definitions}

RETRIEVED EVIDENCE:
{retrieval_evidence_with_source_ids}

RULES:
1. First state what operation, theorem, algorithm, protocol, data structure, language property, or mathematical idea is tested.
2. Select exactly one supplied candidate ID unless evidence is insufficient; then set abstain=true.
3. The selected candidate's Subject, Topic, and Micro-topic must be copied exactly.
4. Do not invent a label or ID. A new micro-topic is only a taxonomy-gap proposal, never an automatic production label.
5. Distinguish close siblings explicitly.
6. If an essential diagram, table, code fragment, or previous-question context is missing, set missing_context=true and abstain=true unless the label is unambiguous without it.
7. Do not use the answer choice as the only evidence.
8. Cite exact terms/formulas/phrases from the question or choices in evidence_spans.
9. Return only the required JSON object.
```

Run at least two independent adjudications for difficult or high-impact records when resources permit. A failed model call is a failure/blocked status, not a semantic decision.

---

## 7. Deterministic acceptance gate

A result may be `accepted` only if every applicable condition passes:

1. The selected candidate ID exists.
2. The exact `(subject, topic, micro_topic)` path exists in the frozen golden taxonomy.
3. Topic belongs to the selected Subject.
4. Micro-topic belongs to the selected Topic.
5. Evidence spans are non-empty and identify actual question evidence.
6. At least one lexical or dense retrieval item supports the candidate.
7. The strongest confusable sibling is rejected with a technically valid reason.
8. Independent votes agree, or a documented adjudicator resolves disagreement.
9. No unresolved essential diagram/table/previous-question defect exists.
10. The micro-topic is at the right granularity and is not merely a duplicate of the Topic.
11. Stability checks do not produce conflicting accepted paths under small prompt/query perturbations.
12. The calibrated acceptance probability is above the predeclared threshold.

If any condition fails:

```text
manual_review  = semantically plausible but proof obligations incomplete
input_defect   = source evidence is incomplete or malformed
blocked        = model/service/hash/taxonomy/pipeline failure
```

Never write an empty `new_concept`, `PENDING_LLM_REVIEW`, or guessed fallback as an accepted result.

Recommended result record:

```json
{
  "source_index": 0,
  "question_id": "GATE_CS_2011:GATE2011.pdf:0",
  "year": 2011,
  "original_subject": "Compiler Design",
  "original_topic": "Lexical Analysis",
  "original_micro_topic": "Keyword and Token Recognition",
  "predicted_subject": "Compiler Design",
  "predicted_topic": "Lexical Analysis",
  "predicted_micro_topic": "Keyword and Token Recognition",
  "selected_candidate_id": "tax_...",
  "changed": false,
  "retrieval_evidence": [],
  "rule_checks": {},
  "model_votes": [],
  "confidence_features": {},
  "calibrated_acceptance_probability": null,
  "decision": "manual_review",
  "reason_codes": [],
  "reasoning": "...",
  "source_hash": "...",
  "audit_version": "semantic-audit-v1"
}
```

For every changed accepted result, also write a human-readable delta entry:

```json
{
  "source_index": 123,
  "question_number": null,
  "year": 2026,
  "question_text_preview": "...",
  "old_subject": "...",
  "old_topic": "...",
  "old_micro_topic": "...",
  "new_subject": "...",
  "new_topic": "...",
  "new_micro_topic": "...",
  "reasoning": "...",
  "decision": "accepted",
  "changed": true
}
```

Question identifiers may be absent in the source (`question_number` was null in the inspected queue). Use a stable ID made from `paper_id`, `file_name`, and source index; do not depend on a missing field.

---

## 8. Gold set, calibration, and non-uniform data

The data is not uniformly distributed. Do not claim that a random sample automatically represents the full label space.

Create a human-verified gold set before calibrating acceptance. Stratify by:

- all Subjects;
- Topics and rare Micro-topics;
- years/papers, with paper/year holdout where possible;
- MCQ, MSQ, and NAT;
- easy and hard questions;
- known confusable pairs;
- records with missing-figure/table cues;
- records flagged by TF-IDF or retrieval disagreement;
- repeated/near-duplicate question families.

Existing labels cannot be the gold labels because they are being audited. A reviewer must read the question and choose the canonical path. Difficult cases should receive a second review.

Do not fit a random row split that leaks near-duplicate questions across training and evaluation. Prefer paper/year-based holdout. Report:

- Subject accuracy;
- Topic accuracy conditional on correct Subject;
- Micro-topic accuracy conditional on correct Subject and Topic;
- exact full-path accuracy;
- accepted-set error rate;
- coverage versus risk;
- calibration error and Brier score if probabilities are used;
- invalid-output rate;
- missing-context detection recall;
- per-subject and rare-label performance.

A model can obtain high subject accuracy while failing micro-topic accuracy. Keep these metrics separate.

Use calibrated features such as:

```text
lexical score,
dense similarity,
RRF score,
reranker score,
top1-top2 margin,
vote agreement,
subject/topic/micro agreement,
syllabus match,
exact technical-token match,
input completeness,
original-label agreement.
```

Calibrate on verified labels using isotonic regression, temperature scaling, or a carefully sized empirical reliability table. Do not call an LLM's self-reported confidence a probability.

---

## 9. Checkpointing and interruption protocol

The run must be resumable and safe:

- Process one question or a very small batch at a time.
- Save every result immediately or at most every few records.
- Use atomic temporary-file replacement (`tempfile` + `os.replace`).
- Keep completed indices and failed indices separately.
- Do not advance `last_processed_index` past a record whose result was not durably written.
- On restart, verify source/taxonomy/syllabus hashes match the manifest.
- If a model call times out, retry with bounded exponential backoff, then mark `blocked`.
- Never mark a failed model call as `changed=false` or as semantically correct.
- Support `--start-index`, `--only-failed`, `--batch-size`, `--run-dir`, and `--dry-run`.
- Preserve raw model responses for auditability, but redact secrets if any service returns them.

Recommended checkpoint fields:

```json
{
  "version": 2,
  "pipeline_version": "semantic-audit-v1",
  "source_sha256": "...",
  "taxonomy_sha256": "...",
  "syllabus_sha256": "...",
  "total_questions": 1621,
  "last_processed_index": -1,
  "completed": 0,
  "accepted": 0,
  "manual_review": 0,
  "input_defect": 0,
  "blocked": 0,
  "results_file": "results.jsonl",
  "updated_at": "..."
}
```

Use JSONL for append-friendly per-question records, plus a separate manifest. A final JSON report can be generated after completion.

---

## 10. Production update policy

Never modify the root `Q.json` during ingestion, taxonomy reconciliation, candidate generation, or pilot runs.

After all accepted records have been reviewed/approved:

1. Copy the original source to a timestamped/versioned backup.
2. Apply only approved accepted mappings.
3. Preserve every non-label field byte-for-byte where practical.
4. Validate that record count remains 1,621.
5. Validate every new path against the frozen golden taxonomy.
6. Validate no question index is duplicated or lost.
7. Generate an old-to-new diff report.
8. Write the new data to a temporary file and atomically replace a versioned output, not the source first.
9. Run application/evaluation tests against the versioned output.
10. Obtain owner approval before replacing production `Q.json`.

Recommended outputs:

```text
E:/GATE PRIDICTION/audit_runs/<run_id>/manifest.json
E:/GATE PRIDICTION/audit_runs/<run_id>/normalized_questions.jsonl
E:/GATE PRIDICTION/audit_runs/<run_id>/classification_results.jsonl
E:/GATE PRIDICTION/audit_runs/<run_id>/delta_report.json
E:/GATE PRIDICTION/audit_runs/<run_id>/manual_review_queue.jsonl
E:/GATE PRIDICTION/audit_runs/<run_id>/validation_report.json
E:/GATE PRIDICTION/Q_semantically_audited_<run_id>.json
```

Do not silently add a new micro-topic. Put it in:

```text
new_taxonomy_candidates.jsonl
```

with evidence, proposed parent Topic, syllabus reference, and approval status. Only after taxonomy review can it be added to the canonical taxonomy and used for a second classification run.

---

## 11. Suggested implementation sequence for the new agent

### Phase 0 — Freeze and inspect

1. Read this file completely.
2. List repository status without deleting or overwriting user files.
3. Read `Q.json`, `golden_taxonomy.json`, and `gate_syllabus.json` with UTF-8.
4. Compute hashes and counts.
5. Inspect `audit_checkpoint.json`; treat it as zero semantic progress unless valid result records prove otherwise.
6. Do not trust historical generated reports as final labels.

### Phase 1 — Taxonomy normalization

1. Normalize the nested golden taxonomy into legal path rows.
2. Parse the flattened `canonical_taxonomy.json` correctly.
3. Compare golden taxonomy to `gate_syllabus.json`.
4. Produce a taxonomy-gap/alias review report.
5. Freeze and hash the reviewed taxonomy.

### Phase 2 — Question/input audit

1. Normalize question text without destroying raw text.
2. Detect diagrams, tables, previous-question references, missing choices, malformed text, and duplicates.
3. Produce an input-quality report.
4. Create stable question IDs.

### Phase 3 — Evidence pilot

1. Build lexical and dense evidence indexes.
2. Seed with a small manually verified set.
3. Test retrieval on 50–100 questions, including hard/confusable cases.
4. Inspect whether retrieved evidence actually supports the candidate.
5. Fix retrieval and alias rules before classification at scale.

### Phase 4 — Gold-set construction

1. Have a reviewer label a stratified sample.
2. Add a second review for disagreements and hard cases.
3. Freeze the gold set before model calibration.

### Phase 5 — Adjudicator pilot

1. Run the exact structured prompt over 50–100 questions.
2. Validate JSON schema and candidate IDs.
3. Run deterministic proof obligations.
4. Review accepted and abstained examples.
5. Measure disagreement and missing-context detection.

### Phase 6 — Calibration

1. Fit the acceptance selector only on verified labels.
2. Use paper/year holdout for evaluation.
3. Choose a threshold for the owner's accepted-set risk target.
4. Publish risk/coverage and per-subject results.
5. If the threshold gives low coverage, keep the low coverage; do not force labels.

### Phase 7 — Full resumable audit

1. Process all 1,621 questions sequentially or with safe workers.
2. Persist every result immediately.
3. Put uncertain cases in the review queue.
4. Continue until every source index is in exactly one terminal state:
   `accepted`, `manual_review`, `input_defect`, or `blocked`.
5. Verify 100% coverage of indices 0 through 1,620.

### Phase 8 — Approval and patch

1. Review all manual cases and new taxonomy candidates.
2. Generate final delta and validation reports.
3. Write a versioned audited dataset.
4. Only then ask for/perform production replacement.

---

## 12. Minimum validation checklist before declaring completion

Do not declare completion until all answers below are true:

- [ ] `Q.json` was not modified during audit preparation.
- [ ] Source, taxonomy, and syllabus hashes are recorded.
- [ ] Exactly 1,621 source records were ingested.
- [ ] Every source index 0–1,620 has exactly one terminal result.
- [ ] Every accepted label is an exact legal Subject -> Topic -> Micro-topic path.
- [ ] No accepted result has unresolved essential missing context.
- [ ] Every changed result has an old-to-new mapping and evidence-grounded reasoning.
- [ ] Every blocked/service failure is visibly marked blocked.
- [ ] Every new taxonomy candidate is separated from production labels.
- [ ] Gold-set labels were independently reviewed.
- [ ] Evaluation uses verified labels, not the original suspicious labels.
- [ ] Calibration and accepted-set risk/coverage are reported.
- [ ] Hard cases and rare labels are represented in validation.
- [ ] A rollback backup exists.
- [ ] The final dataset passes count/path/field integrity checks.
- [ ] Owner approval was obtained before production replacement.

---

## 13. Important final warnings

1. Do not claim that TF-IDF, embeddings, or an LLM response is proof of semantic truth.
2. Do not call the earlier 2026-only workflow a full 2011–2026 audit.
3. Do not call `audit_engine.py` a semantic classifier; it is a queue/checkpoint scaffold.
4. Do not use `run_audit_batch.py` as a completed worker; its normal output is `PENDING_LLM_REVIEW`.
5. Do not use existing labels as gold labels.
6. Do not assume the distribution is uniform.
7. Do not force labels for missing diagrams, tables, or context.
8. Do not add arbitrary new micro-topics silently.
9. Do not overwrite `Q.json` before validation and owner approval.
10. If model capacity runs out, checkpoint and stop safely; never fabricate outputs.

The central design principle is:

```text
Legal taxonomy constraints + question evidence + hierarchical candidate search
+ independent adjudication + deterministic proof checks + calibrated abstention
= an auditable, high-quality training corpus.
```

This is how the question bank can become a dependable gold mine for downstream ML instead of merely becoming a uniformly formatted collection of unverified labels.
