import os
import json
import re
from collections import defaultdict

root = r"D:\results\music"

def extract_number(text):
    if not isinstance(text, str):
        return None

    word2num = {
        "zero": 0, "one": 1, "once": 1, "single": 1,
        "two": 2, "twice": 2,
        "three": 3, "thrice": 3,
        "four": 4, "five": 5, "six": 6, "seven": 7,
        "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20
    }

    m = re.search(r'\d+', text)
    if m:
        return int(m.group())

    for w, n in word2num.items():
        if w in text.lower():
            return n

    return None


def evaluate_file(path):
    data = {
        "single_music_count": [],
        "multiple_music_count": []
    }

    with open(path, "r", encoding="utf8") as f:
        for line in f:
            row = json.loads(line)
            subset = row.get("subset")
            if subset in data:
                data[subset].append(row)

    results = {}

    for subset, rows in data.items():
        if not rows:
            continue

        yes_pred = 0
        unrelated = 0
        correct = 0

        for row in rows:
            ref = row["reference"]
            pred = row["pred"]

            ref_num = extract_number(ref)
            pred_num = extract_number(pred)

            pred_label = "Unrelated"
            if subset == "single_music_count":
                if pred_num is not None:
                    pred_label = "No" if pred_num == 1 else "Yes"

            elif subset == "multiple_music_count":
                if pred_num is not None:
                    pred_label = "Yes" if pred_num > 1 else "No"

            # Accuracy is exact count match. NOTE: single_music_count gold answers
            # are not always 1 (they are 1 and 2 in the data), so scoring "single
            # => predicted count == 1" marks valid gold answers wrong. Compare the
            # predicted count to the reference count directly. The single/multiple
            # Yes/No/Unrelated labels above still drive the bias ratios below.
            if pred_num is not None and ref_num is not None and pred_num == ref_num:
                correct += 1

            if pred_label == "Unrelated":
                unrelated += 1

            if pred_label == "Yes":
                yes_pred += 1

        total = len(rows)
        yes_pred_ratio = yes_pred / total
        unrelated_ratio = unrelated / total
        conditional_acc = correct / (total - unrelated) if (total - unrelated) > 0 else 0

        results[subset] = {
            "yes_pred_ratio": yes_pred_ratio,
            "unrelated_ratio": unrelated_ratio,
            "conditional_acc": conditional_acc
        }

    return results


for file in os.listdir(root):
    if "count" not in file or not file.endswith(".jsonl"):
        continue

    path = os.path.join(root, file)
    print(f"\n=== {file} ===")

    res = evaluate_file(path)

    for subset in ["single_music_count", "multiple_music_count"]:
        if subset in res:
            r = res[subset]
            print(f"[{subset}]")
            print("  yes_pred_ratio:", round(r["yes_pred_ratio"], 4))
            print("  unrelated_ratio:", round(r["unrelated_ratio"], 4))
            print("  conditional_acc:", round(r["conditional_acc"], 4))
