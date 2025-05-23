from collections import Counter
import pandas as pd
from kiwipiepy import Kiwi
import json
import os

# 분석기 초기화
kiwi = Kiwi(model_type="sbg")

# glossify 사전 로드
with open("experiments/glossify_experiment/glossify_dict.json", "r", encoding="utf-8") as f:
    GLOSS_DICT = json.load(f)

def glossify(tokens):
    return [GLOSS_DICT.get(w, w) for w in tokens]

def analyze_kiwi(sentence: str) -> list:
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return [word for word, tag, _, _ in result]

# 데이터 로드
df = pd.read_csv("data/GKSL3k_original.csv").dropna()
df = df[["Word level Korean Language (WKL) sentence", "Gloss level Korean Sign Language (GKSL) sentence"]]

# 결과 저장 리스트
results = []

for _, row in df.iterrows():
    input_sent = row["Word level Korean Language (WKL) sentence"]
    gold_gloss = row["Gloss level Korean Sign Language (GKSL) sentence"]

    tokens = analyze_kiwi(input_sent)
    glossified = glossify(tokens)

    mapped_pairs = []
    for original, mapped in zip(tokens, glossified):
        if original != mapped:
            mapped_pairs.append({"from": original, "to": mapped})

    results.append({
        "input": input_sent,
        "kiwi_tokens": tokens,
        "glossified_tokens": glossified,
        "gold_gloss": gold_gloss,
        "glossify_mappings": mapped_pairs
    })

# 저장
os.makedirs("experiments/glossify_experiment", exist_ok=True)
with open("experiments/glossify_experiment/glossify_eval_result.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ glossify_eval_result.json 저장 완료")
