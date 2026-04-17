import os
import json

folder = r"D:\results\fsd50\two_classification"

results = {}

for fname in os.listdir(folder):
    if not fname.endswith(".jsonl"):
        continue

    file_path = os.path.join(folder, fname)
    total, correct = 0, 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                reference = data.get("reference", "").strip().lower()
                pred = data.get("pred", "").lower()

                if "yes" in pred and reference == "yes":
                    correct += 1
                elif "no" in pred and reference == "no":
                    correct += 1

                total += 1
            except json.JSONDecodeError:
                print(f"[WARN] JSON decode error in file {fname}: {line}")

    accuracy = correct / total if total > 0 else 0.0
    results[fname] = (accuracy, correct, total)
    print(f"{fname}: Accuracy = {accuracy:.2%}  ({correct}/{total})")

output_path = os.path.join(folder, "accuracy_results.txt")
with open(output_path, "w", encoding="utf-8") as out:
    for fname, (accuracy, correct, total) in results.items():
        out.write(f"{fname}: Accuracy = {accuracy:.2%}  ({correct}/{total})\n")

