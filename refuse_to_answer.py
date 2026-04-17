import os
import json
import re
from glob import glob
from collections import defaultdict

REFUSAL_PATTERNS = [
    r"i (can|cannot|can't) (not )?(access|listen|hear|process).*audio",
    r"unable to (access|listen|hear|process).*audio",
    r"as a .*?(language model|text-based).*cannot.*audio",
    r"i (can|cannot|can't).*determine.*audio",
    r"audio.*not.*available",
    r"no audio.*provided",
    r"i'm not able to",
    r"i am not able to",
    r"unable to answer",
    r"cannot answer",
    r"can't answer",
    r"i do not have access",
    r"i don't have access",
    r"i (can|cannot|can't).*analyze audio",
]

REFUSAL_REGEX = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)

def is_refusal(text: str) -> bool:
    if text is None:
        return True
    text = text.strip()
    if len(text) == 0:
        return True
    return REFUSAL_REGEX.search(text) is not None


def analyze_refusal_in_dir(dir_paths):

    results = []

    for root in dir_paths:
        json_files = glob(os.path.join(root, "*.jsonl"))

        for file in json_files:
            total = 0
            refusal_count = 0
            refusal_examples = []

            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        item = json.loads(line)
                    except:
                        continue

                    total += 1
                    pred = item.get("pred", "") or item.get("response", "")

                    if is_refusal(pred):
                        refusal_count += 1
                        if len(refusal_examples) < 5:
                            refusal_examples.append(pred)

            refusal_rate = refusal_count / total if total > 0 else 0

            results.append({
                "file": os.path.basename(file),
                "total": total,
                "refusal": refusal_count,
                "refusal_rate": round(refusal_rate, 4),
                "example": refusal_examples
            })

    return results


if __name__ == "__main__":
    dir_paths = [
        r"D:\results\music\two_classification",
        r"D:\results\music\else",
    ]

    results = analyze_refusal_in_dir(dir_paths)

    print("\n========results ========\n")
    for r in results:
        print(f"file: {r['file']}")
        print(f"  total: {r['total']}")
        print(f"  refusal: {r['refusal']}")
        print(f"  refusal_rate: {r['refusal_rate']}")
        if r["example"]:
            print(f"  example")
            for ex in r["example"]:
                print(f"    - {ex}")
        print("\n")

    print("Finish！")
