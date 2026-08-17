with open("gate_apex_v10.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '        print(f"\n✨ Predicting New MT candidates for {target_year} …")'
replacement = r'        print(f"\n✨ Predicting New MT candidates for {target_year} …")'

text = text.replace(target, replacement)

with open("gate_apex_v10.py", "w", encoding="utf-8") as f:
    f.write(text)
