with open("gate_apex_v10.py", "r", encoding="utf-8") as f:
    text = f.read()

# I will just write a python script to replace the bad function block using standard parsing, or I can just fix the new line.
import re
# Let's restore the backup if any, or just do a raw regex replacement again
