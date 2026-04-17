import os
import re
import json

folder = r"D:\results\audiohallu\else"
results = {}

NUMBER_WORDS = {
    "zero": 0, "one": 1, "once": 1, "single": 1,
    "two": 2, "twice": 2,
    "three": 3, "thrice": 3,
    "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20
}

number_words_sorted = sorted(NUMBER_WORDS.keys(), key=lambda x: -len(x))
number_words_pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in number_words_sorted) + r")\b", flags=re.IGNORECASE)

digit_pattern = re.compile(r"\b(\d+)\b")

def extract_number_from_text(text):
    if not text:
        return None
    m = digit_pattern.search(text)
    if m:
        try:
            return int(m.group(1))
        except:
            pass
    m2 = number_words_pattern.search(text)
    if m2:
        key = m2.group(1).lower()
        return NUMBER_WORDS.get(key)
    return None

CANNOT_HEAR_KEYWORDS = [
    "sorry", "don't have access", "do not have access", "no recording",
    "didn't provide", "did not provide", "cannot access", "i'm not capable",
    "i am not capable", "cannot listen", "cannot hear", "no audio", "no recording provided"
]

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
                subset = data.get("subset", "").strip()
                reference = data.get("reference")
                pred_raw = data.get("pred", "")
                pred = pred_raw.strip().lower()
                total += 1

                if subset == "commonvoice_invalid_gender":
                    ref_is_none = str(reference).strip().lower()
                    if any(k in pred for k in CANNOT_HEAR_KEYWORDS):
                        correct += 1

                elif subset == "commonvoice_word_count":

                    try:
                        ref_num = int(reference)
                    except:
                        ref_num = None
                    pred_num = extract_number_from_text(pred)
                    if pred_num is not None and ref_num is not None and pred_num == ref_num:
                        correct += 1

                elif subset == "speech_commands_comparsion_loudness":
                    ref = str(reference).strip().lower()
                    # 允许不同写法： "the first", "first instance", "first." 等
                    if (("first" in pred) and ("first" in ref)) or (("second" in pred) and ("second" in ref)):
                        # 更严格：pred里若同时出现 first 和 second 则认为不确定 -> 不计正确
                        if ("first" in pred) and ("second" in pred):
                            pass
                        else:
                            if "first" in pred and "first" in ref:
                                correct += 1
                            elif "second" in pred and "second" in ref:
                                correct += 1

                elif subset == "speech_commands_comparsion_speed":
                    ref = str(reference).strip().lower()
                    if (("first" in pred) and ("first" in ref)) or (("second" in pred) and ("second" in ref)):
                        if ("first" in pred) and ("second" in pred):
                            pass
                        else:
                            if "first" in pred and "first" in ref:
                                correct += 1
                            elif "second" in pred and "second" in ref:
                                correct += 1

                elif subset == "invalid_noise":

                    ref_is_none = str(reference).strip().lower()
                    if any(k in pred for k in CANNOT_HEAR_KEYWORDS):
                        correct += 1

                else:
                    print(f"[WARN] 未知 subset：{subset}，文件 {fname}")

            except Exception as e:
                print(f"[ERROR] {fname} line parse error: {e}")

    accuracy = correct / total if total > 0 else 0.0
    results[fname] = (accuracy, correct, total)
    print(f"{fname}: Accuracy = {accuracy:.2%}  ({correct}/{total})")

output_path = os.path.join(folder, "accuracy_results.txt")
with open(output_path, "w", encoding="utf-8") as out:
    for fname, (accuracy, correct, total) in results.items():
        out.write(f"{fname}: Accuracy = {accuracy:.2%}  ({correct}/{total})\n")

