with open("E:/GATE PRIDICTION/run_combined_eval.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("n_new_list = [0, 20, 40, 60]", "n_new_list = [0, 10, 20]")

with open("E:/GATE PRIDICTION/run_combined_eval.py", "w", encoding="utf-8") as f:
    f.write(text)
