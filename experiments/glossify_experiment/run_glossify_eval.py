import pandas as pd
import json
from kiwipiepy import Kiwi

# 🔸 glossify 사전 로드
with open("experiments/glossify_experiment/glossify_dict.json", "r", encoding="utf-8") as f:
    GLOSS_DICT = json.load(f)

# 🔸 glossify 함수 정의
def glossify(tokens):
    return [GLOSS_DICT.get(w, w) for w in tokens]

# 🔸 Kiwi 분석기 설정
kiwi = Kiwi(model_type="sbg")

def analyze_kiwi(sentence: str) -> list:
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return [word for word, tag, _, _ in result]

# 🔸 데이터 로드
df = pd.read_csv("data/GKSL3k_original.csv").dropna()
df = df[["Word level Korean Language (WKL) sentence", "Gloss level Korean Sign Language (GKSL) sentence"]]

# 🔸 결과 비교 출력
for _, row in df.sample(10, random_state=42).iterrows():
    input_sent = row["Word level Korean Language (WKL) sentence"]
    gold_gloss = row["Gloss level Korean Sign Language (GKSL) sentence"]

    tokens = analyze_kiwi(input_sent)
    glossified = glossify(tokens)

    print("🟡 입력:", input_sent)
    print("🔹 Kiwi 결과:", " ".join(tokens))
    print("🟢 Glossify 결과:", " ".join(glossified))
    print("✅ 정답 gloss:", gold_gloss)

    print("📌 매핑:")
    for original, mapped in zip(tokens, glossified):
        if original != mapped:
            print(f"  {original} → {mapped}")
    print("-" * 60)
