from kiwipiepy import Kiwi
import MeCab

# 분석기 설정
kiwi = Kiwi(model_type="sbg")
mecab = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/mecab-ko-dic -r /opt/homebrew/etc/mecabrc')

# 문장 리스트
sentences = [
    "긴 주행이 예상된다면 여분의 기름을 가져가는 것도 좋겠어요.",
    "네, 아침 식사가 포함되어 있습니다. 1층 식당에서 아침마다 다양한 메뉴를 제공하고 있습니다.",
    "셋이 같이 와서 3명의 스키 장비도 같이 빌리려고 해요.",
    "지금 7호선 지하철 운행은 어떻게 되고 있나요?",
    "여행 가기 전에 짐을 싸야 하는데 나는 그게 너무 귀찮아."
]

# 분석 함수 정의
def mecab_analyze(sentence):
    lines = mecab.parse(sentence).split("\n")
    words = []
    for line in lines:
        if line == "EOS" or line == "":
            continue
        try:
            token, feature = line.split("\t")
            pos = feature.split(",")[0]
            words.append(f"{token}/{pos}")
        except:
            continue
    return " ".join(words)

def kiwi_analyze(sentence):
    result = kiwi.analyze(sentence, top_n=1)[0][0]
    return " ".join([f"{word}/{tag}" for word, tag, _, _ in result])

# 결과 저장
results = []
for s in sentences:
    results.append({
        "문장": s,
        "MeCab": mecab_analyze(s),
        "Kiwi": kiwi_analyze(s)
    })

print(results)

import pandas as pd

# 입력된 결과 리스트
data = [
    {'문장': '긴 주행이 예상된다면 여분의 기름을 가져가는 것도 좋겠어요.', 'MeCab': '긴/VA+ETM 주행/NNG 이/JKS 예상/NNG 된다면/XSV+EC 여분/NNG 의/JKG 기름/NNG 을/JKO 가져가/VV 는/ETM 것/NNB 도/JX 좋/VA 겠/EP 어요/EF ./SF', 'Kiwi': '길/VA ᆫ/ETM 주행/NNG 이/JKS 예상/NNG 되/XSV ᆫ다면/EC 여분/NNG 의/JKG 기름/NNG 을/JKO 가져가/VV 는/ETM 것/NNB 도/JX 좋/VA 겠/EP 어요/EF ./SF'},
    {'문장': '네, 아침 식사가 포함되어 있습니다. 1층 식당에서 아침마다 다양한 메뉴를 제공하고 있습니다.', 'MeCab': '네/IC ,/SC 아침/NNG 식사/NNG 가/JKS 포함/NNG 되/XSV 어/EC 있/VX 습니다/EF ./SF 1/SN 층/NNG 식당/NNG 에서/JKB 아침/NNG 마다/JX 다양/XR 한/XSA+ETM 메뉴/NNG 를/JKO 제공/NNG 하/XSV 고/EC 있/VX 습니다/EF ./SF', 'Kiwi': '네/IC ,/SP 아침/NNG 식사/NNG 가/JKS 포함/NNG 되/XSV 어/EC 있/VX 습니다/EF ./SF 1/SN 층/NNG 식당/NNG 에서/JKB 아침/NNG 마다/JX 다양/NNG 하/XSA ᆫ/ETM 메뉴/NNG 를/JKO 제공/NNG 하/XSV 고/EC 있/VX 습니다/EF ./SF'},
    {'문장': '셋이 같이 와서 3명의 스키 장비도 같이 빌리려고 해요.', 'MeCab': '셋/NR 이/JKS 같이/MAG 와서/VV+EC 3/SN 명/NNBC 의/JKG 스키/NNG 장비/NNG 도/JX 같이/MAG 빌리/VV 려고/EC 해요/VX+EF ./SF', 'Kiwi': '셋/NR 이/JKS 같이/MAG 오/VV 어서/EC 3/SN 명/NNB 의/JKG 스키/NNG 장비/NNG 도/JX 같이/MAG 빌리/VV 려고/EC 하/VX 어요/EF ./SF'},
    {'문장': '지금 7호선 지하철 운행은 어떻게 되고 있나요?', 'MeCab': '지금/MAG 7/SN 호/NNBC 선/NNG 지하철/NNG 운행/NNG 은/JX 어떻게/MAG 되/VV 고/EC 있/VX 나요/EF ?/SF', 'Kiwi': '지금/MAG 7/SN 호/NNB 선/NNG 지하철/NNG 운행/NNG 은/JX 어떻/VA-I 게/EC 되/VV 고/EC 있/VA 나요/EF ?/SF'},
    {'문장': '여행 가기 전에 짐을 싸야 하는데 나는 그게 너무 귀찮아.', 'MeCab': '여행/NNG 가/VV 기/ETN 전/NNG 에/JKB 짐/NNG 을/JKO 싸/VV 야/EC 하/VV 는데/EC 나/NP 는/JX 그게/NP+JKS 너무/MAG 귀찮/VA 아/EF ./SF', 'Kiwi': '여행/NNG 가/VV 기/ETN 전/NNG 에/JKB 짐/NNG 을/JKO 싸/VV 어야/EC 하/VX 는데/EC 나/NP 는/JX 그것/NP 이/JKS 너무/MAG 귀찮/VA 어/EF ./SF'}
]

# DataFrame으로 변환
df = pd.DataFrame(data)

# 테이블로 표시
import ace_tools_open as tools; tools.display_dataframe_to_user(name="형태소 분석기 결과 비교", dataframe=df)
