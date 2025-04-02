import pandas as pd
import MeCab
from kiwipiepy import Kiwi


# Kiwi 설정
kiwi = Kiwi()

def kiwi_analyze(sentence: str) -> list:
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return [word for word, tag, _, _ in result if not tag.startswith("J") and not tag.startswith("E") and tag != "SF"]

# MeCab 설정
mecab = MeCab.Tagger(
    '-d /opt/homebrew/lib/mecab/dic/mecab-ko-dic -r /opt/homebrew/etc/mecabrc'
)

def mecab_analyze(sentence: str) -> list:
    lines = mecab.parse(sentence).split("\n")
    words = []
    for line in lines:
        if line == "EOS" or line == "":
            continue
        token, feature = line.split("\t")[0], line.split("\t")[1]
        pos = feature.split(",")[0]
        if pos not in ["JKS", "JKB", "JX", "EF", "EC", "SF"]:
            words.append(token)
    return words


# 기타 처리 함수 (현재는 그대로 사용)
def reorder(words): return words
def glossify(words): return words

# 데이터 불러오기
df = pd.read_csv("data/GKSL3k_original.csv")
df = df[["Word level Korean Language (WKL) sentence", "Gloss level Korean Sign Language (GKSL) sentence"]].dropna()
samples = df.sample(20, random_state=42)

# 비교 실행
for _, row in samples.iterrows():
    input_sentence = row["Word level Korean Language (WKL) sentence"]
    expected_gloss = row["Gloss level Korean Sign Language (GKSL) sentence"]
    mecab_pred = " ".join(glossify(reorder(mecab_analyze(input_sentence))))
    kiwi_pred = " ".join(glossify(reorder(kiwi_analyze(input_sentence))))

    print("🟡 입력:", input_sentence)
    print("✅ 정답:", expected_gloss)
    print("🔵 MeCab 예측:", mecab_pred)
    print("🟢 Kiwi 예측:", kiwi_pred)
    print("-" * 50)
