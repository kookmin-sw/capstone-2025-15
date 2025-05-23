from kiwipiepy import Kiwi

kiwi = Kiwi(model_type="sbg")

def analyze_sentence(sentence: str):
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return [(word, tag) for word, tag, _, _ in result]

def print_analysis(sentence: str):
    print(f"\n🟡 입력: {sentence}")
    tokens = analyze_sentence(sentence)
    print("🔍 분석 결과:", " | ".join([f"{w}/{t}" for w, t in tokens]))
    return tokens

sample = "지하철을 타고 가다가 신호등 앞에서 내렸어요."
print_analysis(sample)