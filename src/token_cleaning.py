from kiwipiepy import Kiwi

# Kiwi 분석기 설정
kiwi = Kiwi(model_type="sbg")

# 제거할 불필요한 품사 접두어
UNWANTED_POS_PREFIX = {"J", "E", "S", "X"}
# 제거할 1글자 불용어 리스트 (의미 없음)
STOPWORDS = {"다", "요", "좀", "어", "이요", "나요", "께서", "?"}

def analyze_kiwi_raw(sentence: str):
    #형태소 분석 결과를 (형태소, 품사) 튜플 리스트로 반환
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return [(word, tag) for word, tag, _, _ in result]

def analyze_kiwi_clean(sentence: str):
    #불용어 제거, 의미 있는 품사만 필터링한 결과를 반환
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    filtered = [
        word for word, tag, _, _ in result
        if tag[0] not in UNWANTED_POS_PREFIX and word not in STOPWORDS and len(word) > 1
    ]
    return filtered