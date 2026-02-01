import re
import shutil
from datetime import datetime

orig = 'Q.json'
backup = f"Q.json.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
shutil.copyfile(orig, backup)
print(f'Backed up {orig} -> {backup}')

with open(orig, 'r', encoding='utf-8') as f:
    text = f.read()

# Merge multiple top-level arrays by replacing occurrences like ']\n[' or ']   \n   [' with ',\n'
fixed = re.sub(r"\]\s*\n\s*\[", ',\n', text)

# Ensure file still starts with '[' and ends with ']'
fixed = fixed.strip()
if not fixed.startswith('['):
    fixed = '[\n' + fixed
if not fixed.endswith(']'):
    fixed = fixed + '\n]'

with open(orig, 'w', encoding='utf-8') as f:
    f.write(fixed)

print('Wrote fixed Q.json')
