# 🧪 Tokenizer Comparison (Kiwi vs MeCab)

## 📌 실험 목적
이 실험은 형태소 분석기 **Kiwi**와 **MeCab**을 비교하여, 
한국어 수어(gloss) 전처리에 어떤 분석기가 더 적합한지를 평가하기 위한 실험입니다.

특히 형태소 분석 과정에서 **의미 단위가 명확하게 분리**되고, 
**불필요한 조사나 어미 등의 처리가 얼마나 효과적으로 이뤄지는지**를 중심으로 비교합니다.

> ✅ 이 실험은 [kiwipiepy 공식 disambiguate benchmark](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/disambiguate)를 기반으로 참고 및 재구성되었습니다.

---

## 🔍 실험 배경
- 형태소 분석기는 수어 gloss 생성 파이프라인의 **1단계**로 사용됨
- 전처리 성능이 이후 단계인 `reorder` 및 `glossify`의 성능에 큰 영향을 미침
- 기존에는 단어만 추출하고 있었으나, 분석기별 **품사 태그와 형태 정보까지 비교**하여 전처리 기준을 수립하고자 함

---

## 🧪 평가 항목
- ✅ 분석기 결과의 단어 정확도
- ✅ 품사 태깅의 일관성과 유용성
- ✅ 조사/어미 제거가 자연스러운가?
- ✅ 형태소 분리 시 의미 단위가 명확히 구분되는가?

---

## 🧾 평가 방식
- **데이터**: `data/GKSL3k_original.csv`에서 샘플 20개 추출
- **비교 대상**: MeCab, Kiwi
- **분석 결과**: 단어 리스트 및 품사 태그 출력
- **정답 비교**: gloss와 단어 비교를 통해 유사도 간접 평가
- **향후 계획**: BLEU, Jaccard 등 정량 지표 도입 예정

---

## 🧠 실험 결과 요약
- Kiwi는 조사 제거 성능이 높고, 일부 동사를 간결하게 처리함
- MeCab은 단어가 더 세분화되지만, 어미/조사가 포함되는 경향
- 둘 다 전처리만으로는 gloss 정답과 1:1 매핑은 어려움 (추가 룰 필요)

---

## 🔜 다음 작업 계획
- [x] 분석 결과 기반 불용어 제거 기준 설계
- [ ] `glossify()` 함수에 의미 기반 단어 매핑 로직 도입
- [ ] `reorder()` 모듈을 활용한 단어 순서 재구성 실험
- [ ] Kiwi vs MeCab의 gloss 예측 정확도 비교 (BLEU 등)

---

## 📂 참고 자료
- 📁 [benchmark/disambiguate](https://github.com/bab2min/kiwipiepy/tree/main/benchmark/disambiguate)
- 📈 [benchmark results](https://github.com/bab2min/kiwipiepy/blob/main/benchmark/disambiguate/results.md)

