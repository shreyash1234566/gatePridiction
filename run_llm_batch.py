import json
import os
import sys

def format_taxonomy(golden_tax):
    out = ""
    for c, data in golden_tax.items():
        out += f"- Concept: {c}\n"
        for mt in data.get("micro_topics", []):
            out += f"    * {mt}\n"
    return out

def generate_prompts(start, batch_size):
    with open('Q.json', 'r', encoding='utf-8') as f:
        q_data = json.load(f)
    with open('golden_taxonomy.json', 'r', encoding='utf-8') as f:
        golden = json.load(f)
    
    end = min(start + batch_size, len(q_data))
    prompts = []
    
    # We will generate a single large prompt sequence that processing 50 in one shot is too long
    # We'll just generate the first 10 for safety tests.
    pass

if __name__ == "__main__":
    pass
