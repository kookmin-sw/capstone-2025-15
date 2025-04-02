import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from analyzer import analyze
from reorder import reorder
from glossary import glossify

import MeCab
import pandas as pd

tagger = MeCab.Tagger(
    '-d /opt/homebrew/lib/mecab/dic/mecab-ko-dic -r /opt/homebrew/etc/mecabrc'
)

analyze.__globals__["tagger"] = tagger

# 데이터 불러오기
df = pd.read_csv("data/GKSL3k_original.csv")
df = df[["Word level Korean Language (WKL) sentence", "Gloss level Korean Sign Language (GKSL) sentence"]].dropna()

# 샘플링
samples = df.sample(10, random_state=42)

# 테스트 실행
for _, row in samples.iterrows():
    input_sentence = row["Word level Korean Language (WKL) sentence"]
    expected_gloss = row["Gloss level Korean Sign Language (GKSL) sentence"]
    predicted = " ".join(glossify(reorder(analyze(input_sentence))))
    
    print("입력:", input_sentence)
    print("예측:", predicted)
    print("정답:", expected_gloss)
    print("-" * 50)
