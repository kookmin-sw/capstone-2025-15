from kiwipiepy import Kiwi

# Kiwi 분석기 설정
kiwi = Kiwi(model_type="sbg")

# 제거할 불필요한 품사 태그 (정확히 명시)
UNWANTED_TAGS = {
    # 조사
    "JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC",
    # 어미
    "EP", "EF", "EC", "ETN", "ETM",
    # 기호 및 특수문자
    "SF", "SP", "SS", "SSO", "SSC", "SE", "SO", "SW",
    # 접사
    "XPN", "XSN", "XSV", "XSA"
}

# 제거할 1글자 불용어 리스트
STOPWORDS = {"다", "요", "좀", "어", "이요", "나요", "께서", "?"}

def analyze_kiwi_raw(sentence: str):
    """
    형태소 분석 결과를 (형태소, 품사) 튜플 리스트로 반환
    """
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return [(word, tag) for word, tag, _, _ in result]

def analyze_kiwi_clean(sentence: str):
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    filtered = []
    for word, tag, _, _ in result:
        if tag in {"NNG", "NNP", "VV", "VA", "VX", "XR"}:
            filtered.append(word)
        elif tag in UNWANTED_TAGS or word in STOPWORDS:
            continue
        elif len(word) > 1:
            filtered.append(word)
    return filtered



if __name__ == "__main__":
    test_sent = "홍수가 나서 집이 물에 잠기고 있어요."
    #test_sent = "고속도로에서 자동차가 갑자기 멈췄어요."

    print("🟡 입력 문장:", test_sent)

    raw = analyze_kiwi_raw(test_sent)
    print("\n🔍 분석 결과 (원본):")
    print(" | ".join([f"{w}/{t}" for w, t in raw]))

    clean = analyze_kiwi_clean(test_sent)
    print("\n✅ 분석 결과 (불용어 제거):")
    print(" | ".join(clean))
