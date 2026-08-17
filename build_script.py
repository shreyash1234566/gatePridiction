import json

with open("audit_args.json", "r", encoding="utf-8") as f:
    args_data = json.load(f)

# Serialize cleanly
qData_str = json.dumps(args_data["questions"], indent=2)
golden_str = json.dumps(args_data["golden"], indent=2)

script = f"""export const meta = {{
  name: 'audit-2026-labels',
  description: 'Audits the 130 questions from 2026',
  phases: [{{title: 'Semantic Audit'}}]
}}

const qData = {qData_str};
const golden = {golden_str};

const AUDIT_SCHEMA = {{
  type: "object",
  properties: {{
    is_correctly_labeled: {{ type: "boolean", description: "True if the original Concept/Micro-topic accurately describe the core CS test concept. False if it is a classification mislabeling or hallucination." }},
    reasoning: {{ type: "string" }},
    suggested_concept: {{ type: "string", description: "The CORRECT concept from the provided Subject taxonomy." }},
    suggested_micro_topic: {{ type: "string", description: "The CORRECT micro-topic from the provided taxonomy. If it is genuinely a new technique, you may use a new concise label." }}
  }},
  required: ["is_correctly_labeled", "reasoning", "suggested_concept", "suggested_micro_topic"]
}}

const results = await pipeline(
  qData,
  async (q, original, idx) => {{
    const subjTax = golden[q.subject] || {{}}
    const prompt = `You are a GATE Computer Science examiner performing a strict semantic audit.

Here is a question from the 2026 exam.
Subject: "${{q.subject}}"
Original Assigned Label:
- Concept (Topic): ${{q.topic}}
- Micro-topic: ${{q.micro_topic}}

Question Text Extract:
${{q.question_text}}
Choices: ${{JSON.stringify(q.choices)}}

Golden Taxonomy for this subject:
${{JSON.stringify(subjTax, null, 2)}}

TASK:
1. Check if the Original Label correctly matches the question semantics. (e.g., CPU vs Disk Scheduling, Array vs CPU, etc.).
2. If wrong OR wrongly specific, select the TRUE Concept and Micro-topic from the Golden Taxonomy. You can propose a new specific micro-topic only if it truly isn't covered.`

    const auditResult = await agent(prompt, {{
      label: `Audit: Q${{q.question_number}} (${{q.subject}})`,
      phase: 'Semantic Audit',
      schema: AUDIT_SCHEMA,
      effort: 'low'
    }})

    return {{
      question_id: q.question_number,
      subject: q.subject,
      old_concept: q.topic,
      old_micro: q.micro_topic,
      ...auditResult
    }}
  }}
)

const deltaReport = results.filter(r => r && !r.is_correctly_labeled)
return deltaReport
"""

with open("audit_2026_compiled.js", "w", encoding="utf-8") as f:
    f.write(script)

print("Created audit_2026_compiled.js successfully")
