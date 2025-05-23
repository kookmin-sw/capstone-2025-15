import os
import json
import csv
import re

# 입력 폴더 및 출력 파일 경로
INPUT_DIR = "data/01_NIKL_Sign Language Parallel Corpus_2023"
OUTPUT_RAW_PATH = "data/ksl_gloss_dataset.csv"
OUTPUT_CLEANED_PATH = "data/ksl_gloss_dataset_cleaned.csv"

results_raw = []
results_cleaned = []

# 🔧 숫자 및 # 제거 함수
def clean_gloss_token(gloss):
    return re.sub(r"\d+#?$", "", gloss.strip())

def clean_glosses(gloss_str):
    return ", ".join([clean_gloss_token(g) for g in gloss_str.split(",")])

# 🔄 JSON 파일 순회
for filename in os.listdr(INPUT_DIR):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(INPUT_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            continue

    korean = data.get("krlgg_sntenc", {}).get("koreanText", "").strip()
    gestures = data.get("sign_script", {}).get("sign_gestures_strong", [])
    glosses = [g.get("gloss_id") for g in gestures if g.get("gloss_id")]

    if korean and glosses:
        gloss_str = ", ".join(glosses)
        results_raw.append({"korean": korean, "glosses": gloss_str})
        results_cleaned.append({"korean": korean, "glosses": clean_glosses(gloss_str)})

# 저장: 원본 gloss 포함
with open(OUTPUT_RAW_PATH, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["korean", "glosses"])
    writer.writeheader()
    writer.writerows(results_raw)

# 저장: 숫자 및 # 제거된 gloss 포함
with open(OUTPUT_CLEANED_PATH, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["korean", "glosses"])
    writer.writeheader()
    writer.writerows(results_cleaned)

print(f"✅ 저장 완료: {len(results_cleaned)}개 샘플 → {OUTPUT_CLEANED_PATH}")
