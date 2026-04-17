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
        "tonic_count": [],
        "stroke_count": []
    }

    # 读取 jsonl
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

            if subset == "tonic_count":
                ref_label = "No"
                if pred_num is None:
                    pred_label = "Unrelated"
                else:
                    pred_label = "No" if pred_num == 1 else "Yes"

                if pred_label == "No" and ref_label == "No" and pred_num == 1:
                    correct += 1

            elif subset == "multiple_music_count":
                ref_label = "Yes"

                if pred_num is None:
                    pred_label = "Unrelated"
                else:
                    pred_label = "Yes" if pred_num > 1 else "No"

                if pred_num == ref_num and ref_num > 1:
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