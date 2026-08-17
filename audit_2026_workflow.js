export const meta = {
  name: 'audit-2026-labels',
  description: 'Audits the 130 questions from 2026 against the newly established Golden Taxonomy to catch classification hallucinations.',
  phases: [{title: 'Semantic Audit'}]
}

const qData = args.questions
const golden = args.golden

const AUDIT_SCHEMA = {
  type: "object",
  properties: {
    is_correctly_labeled: {
      type: "boolean",
      description: "True if the original Concept/Micro-topic accurately describe the core CS test concept. False if it is a classification hallucination."
    },
    reasoning: {
      type: "string",
      description: "A 1-2 sentence explanation of what mathematical or computing concept the question text is actually testing."
    },
    suggested_concept: {
      type: "string",
      description: "The CORRECT concept from the provided Subject taxonomy."
    },
    suggested_micro_topic: {
      type: "string",
      description: "The CORRECT micro-topic from the provided taxonomy. If it is genuinely a new technique, you may use a new concise label."
    }
  },
  required: ["is_correctly_labeled", "reasoning", "suggested_concept", "suggested_micro_topic"]
}

const results = await pipeline(
  qData,
  async (q, original, idx) => {
    const subjTax = golden[q.subject] || {}

    const prompt = `You are an expert GATE Computer Science examiner performing a strict semantic audit.

Here is a question from the 2026 exam in the subject: "${q.subject}"
Original Label Assigned:
- Concept: ${q.topic}
- Micro-topic: ${q.micro_topic}

Question Text Extract:
${q.question_text}
Choices: ${JSON.stringify(q.choices)}

Here is the officially approved "Golden Taxonomy" for this subject:
${JSON.stringify(subjTax, null, 2)}

TASK:
1. Read the Question Text. What specific algorithmic, mathematical, or computing technique is it actually testing?
2. Check if the Original Label correctly matches the question semantics. (NOTE: "Concept" is the broad family; "Micro-topic" is the specific technique).
3. If the Original Label is wrong OR uses the wrong granularity, select the TRUE Concept and Micro-topic from the Golden Taxonomy. If the tested technique genuinely does not exist in the taxonomy, create a precise, highly-specific new micro-topic name under the correct Concept.`

    const auditResult = await agent(prompt, {
      label: `Audit: Q${q.question_number} (${q.subject})`,
      phase: 'Semantic Audit',
      schema: AUDIT_SCHEMA,
      effort: 'low'
    })

    return {
      question_id: q.question_number,
      subject: q.subject,
      old_concept: q.topic,
      old_micro: q.micro_topic,
      ...auditResult
    }
  }
)

const deltaReport = results.filter(r => r && !r.is_correctly_labeled)

return { total: qData.length, flagged: deltaReport.length, deltas: deltaReport }
