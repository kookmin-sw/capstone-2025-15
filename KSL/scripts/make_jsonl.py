import pandas as pd
import MeCab
import json

# 분석기 설정
tagger = MeCab.Tagger(
    '-d /opt/homebrew/lib/mecab/dic/mecab-ko-dic -r /opt/homebrew/etc/mecabrc'
)

def analyze(sentence: str) -> list:
    lines = tagger.parse(sentence).split("\n")
    words = []
    for line in lines:
        if line == "EOS" or line == "":
            continue
        token, feature = line.split("\t")[0], line.split("\t")[1]
        pos = feature.split(",")[0]
        if pos not in ["JKS", "JKB", "JX", "EF", "EC", "SF"]:
            words.append(token)
    return words

# CSV 불러오기
df = pd.read_csv("data/GKSL3k_original.csv")
df = df[["Word level Korean Language (WKL) sentence", "Gloss level Korean Sign Language (GKSL) sentence"]].dropna()

# 전처리 및 jsonl 저장
with open("data/ksl_gloss_dataset.jsonl", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        input_sent = row["Word level Korean Language (WKL) sentence"]
        output_sent = row["Gloss level Korean Sign Language (GKSL) sentence"]
        input_processed = " ".join(analyze(input_sent))
        json.dump({"input": input_processed, "output": output_sent}, f, ensure_ascii=False)
        f.write("\n")

print("저장 완료: data/ksl_gloss_dataset.jsonl")
