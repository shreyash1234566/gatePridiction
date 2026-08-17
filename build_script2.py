import json
import re

with open("audit_args.json", "r", encoding="utf-8") as f:
    args_data = json.load(f)

# Strip control characters from strings
def clean_string(val):
    if isinstance(val, str):
        # Remove all ASCII control characters except \n, \r, \t
        return re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', val)
    elif isinstance(val, list):
        return [clean_string(v) for v in val]
    elif isinstance(val, dict):
        return {k: clean_string(v) for k, v in val.items()}
    return val

args_data = clean_string(args_data)

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
    const prompt = `You are a strict semantic computing examiner.

Examine this 2026 question for: "${{q.subject}}"
Original Label: Concept=${{q.topic}} | Micro-topic=${{q.micro_topic}}

Question:
${{q.question_text}}
Choices: ${{JSON.stringify(q.choices)}}

Taxonomy Allowed:
${{JSON.stringify(subjTax, null, 2)}}

TASK: Check if Original Label matches perfectly. If mathematically or computationally wrong, assign the true Concept/Micro-topic from taxonomy.`

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

return results.filter(r => r && !r.is_correctly_labeled)
"""

# Must write exactly as a literal
with open("audit_2026_compiled.js", "w", encoding="utf-8") as f:
    f.write(script)
print("File scrubbed and generated.")
