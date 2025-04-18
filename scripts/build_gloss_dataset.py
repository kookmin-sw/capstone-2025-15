import os
import json
import csv

# 입력 JSON들이 들어있는 디렉토리
INPUT_DIR = "data/01_NIKL_Sign Language Parallel Corpus_2023"
OUTPUT_PATH = "data/ksl_gloss_dataset.csv"

results = []

for filename in os.listdir(INPUT_DIR):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(INPUT_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ JSON 파싱 실패: {filename}")
            continue

    # ① 한국어 문장
    korean = data.get("krlgg_sntenc", {}).get("koreanText", "").strip()

    # ② 수어 gloss 리스트 추출
    gestures = data.get("sign_script", {}).get("sign_gestures_strong", [])
    glosses = [g.get("gloss_id") for g in gestures if g.get("gloss_id")]

    if korean and glosses:
        results.append({
            "korean": korean,
            "glosses": ", ".join(glosses)
        })

# 저장
with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["korean", "glosses"])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ 추출 완료: {len(results)}개 샘플 저장됨 → {OUTPUT_PATH}")
