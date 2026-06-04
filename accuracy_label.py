import os
import json

# Accuracy for the label-answer tasks that none of the other scripts score:
#   sound_subset/comparison_loudness          -> reference is the louder sound's label
#   music_subset/speech_music_classification   -> reference is "speech" / "music"
# accuracy_classify.py only handles yes/no, accuracy_else.py only handles a fixed
# set of speech subsets, and yesno_bias_test.py only handles the count subsets, so
# these label tasks were previously unscored. A prediction is counted correct when
# the (case-insensitive) reference label appears in it -- the same simple
# substring style used by the other scripts.
#
# NOTE: this is a substring match, so for tasks whose candidate labels overlap
# (e.g. "Guitar" vs "Electric_guitar") it can over-credit. It matches the matching
# style already used in this repo; a stricter exact/token match could be swapped in.

folder = r"D:\results\label"

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
                reference = str(data.get("reference", "")).strip().lower()
                pred = str(data.get("pred", "")).lower()
                if reference and reference in pred:
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
