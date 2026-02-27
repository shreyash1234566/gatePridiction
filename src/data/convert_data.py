import re

# Read data.js
with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the GATE_DATA object
match = re.search(r'const GATE_DATA = ({.*})', content, re.DOTALL)
if match:
    data_content = match.group(1)
    
    # Create TypeScript version
    ts_content = '''// GATE 2027 Comprehensive Website Data
// Auto-generated from data.js
// Contains: PYQs, Predictions, Trends, Statistics, Mock Paper Config

export const GATE_DATA = ''' + data_content + ''';
'''
    
    with open('rawData.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ rawData.ts updated successfully!")
    print(f"   Size: {len(ts_content)/1024:.1f} KB")
else:
    print("❌ Could not find GATE_DATA in data.js")
