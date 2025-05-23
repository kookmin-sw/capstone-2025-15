import os
import csv
import MeCab
from kiwipiepy import Kiwi

# 평가셋 경로
TESTSET_DIR = "experiments/tokenizer_comparison/testset"
RESULT_PATH = "experiments/tokenizer_comparison/results.csv"

# Kiwi 설정 - Semi-BiGRU 기반 성능 모델 사용
#kiwi = Kiwi()
kiwi = Kiwi(model_type="sbg")
 
def kiwi_analyze(sentence: str) -> list:
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return [(word, tag) for word, tag, _, _ in result]

# MeCab 설정
mecab = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/mecab-ko-dic -r /opt/homebrew/etc/mecabrc')

def mecab_analyze(sentence: str) -> list:
    lines = mecab.parse(sentence).split("\n")
    words = []
    for line in lines:
        if line == "EOS" or line == "":
            continue
        try:
            token, feature = line.split("\t")
            pos = feature.split(",")[0]
            words.append((token, pos))
        except:
            print("⚠️ Parse error in line:", line)
    return words

# 평가 데이터셋 로드
def load_dataset(path):
    dataset = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                answer, exam = line.split("\t")
                answer_word, answer_tag = answer.split("/")
                dataset.append(((answer_word, answer_tag), exam))
            except:
                print(f"⚠️ Parse error: {line}")
    return dataset

# 평가 함수
def evaluate(dataset, analyzer):
    correct, total = 0, 0
    for answer, sentence in dataset:
        tokens = analyzer(sentence)
        if answer in tokens:
            correct += 1
        total += 1
    return correct / total if total else 0

# 분석기 리스트
models = {
    "MeCab": mecab_analyze,
    "Kiwi": kiwi_analyze
}

# 평가 실행 및 저장
results = []
for filename in sorted(os.listdir(TESTSET_DIR)):
    if not filename.endswith(".txt"): continue
    path = os.path.join(TESTSET_DIR, filename)
    dataset = load_dataset(path)
    row = [filename]
    print(f"\n📂 {filename}")
    for name, func in models.items():
        acc = evaluate(dataset, func)
        row.append(f"{acc:.3f}")
        print(f"{name}: {acc:.3f}")
    results.append(row)

# CSV 저장
with open(RESULT_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Testset", *models.keys()])
    writer.writerows(results)
    print(f"\n✅ 평가 결과 저장 완료 → {RESULT_PATH}")


# 특정 문장을 대상으로 두 분석기의 결과를 출력해보자
sample_sentence = "저는 점심을 아직 안 먹어서 배가 고파요."

print("\n🧪 분석기별 결과 비교:")
print(f"문장: {sample_sentence}")

# MeCab 결과
mecab_result = mecab_analyze(sample_sentence)
print("\n📌 MeCab 결과:")
for token, pos in mecab_result:
    print(f"{token}\t{pos}")

# Kiwi 결과
kiwi_result = kiwi_analyze(sample_sentence)
print("\n📌 Kiwi 결과:")
for token, pos in kiwi_result:
    print(f"{token}\t{pos}")
