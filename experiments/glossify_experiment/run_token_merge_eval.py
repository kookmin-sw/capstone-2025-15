import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pandas as pd
import json
from src.token_cleaning import analyze_kiwi_clean
from src.token_merge import recombine_tokens


# 데이터 로드
df = pd.read_csv("data/GKSL3k_original.csv").dropna()
df = df[["Word level Korean Language (WKL) sentence", "Gloss level Korean Sign Language (GKSL) sentence"]]

results = []

for _, row in df.sample(20, random_state=42).iterrows():
    sent = row["Word level Korean Language (WKL) sentence"]
    gold = row["Gloss level Korean Sign Language (GKSL) sentence"]

    cleaned = analyze_kiwi_clean(sent)
    merged = recombine_tokens(cleaned)

    results.append({
        "input": sent,
        "cleaned_tokens": cleaned,
        "merged_tokens": merged,
        "gold_gloss": gold
    })

    print("🟡 입력 문장:", sent)
    print("🔹 정제 후 토큰:", cleaned)
    print("🔧 병합 결과:", merged)
    print("✅ 정답 gloss:", gold)
    print("-" * 60)
