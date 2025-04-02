---
name: 아바타 기능 개발
about: 아바타 생성, keypoint 수신, Unity 연동 등 관련 작업
title: "[Avatar] "
labels: avatar, feature
assignees: ''
---

## 👤 작업 설명
아바타 구현과 관련된 작업 내용을 작성해주세요.

예시:
- gloss-to-keypoint 데이터 연동
- 프레임별 키포인트 해석 → 애니메이션 적용
- Unity에서 프레임 수신 처리
- 얼굴 표정 / 손 모양 분리 처리 등

## 📁 작업 위치
예: 
- avatar/gloss_to_keypoint.py  
- Unity/Assets/Scripts/Receiver.cs  

## ✅ 작업 체크리스트
- [ ] gloss-to-keypoint JSON 포맷 정의
- [ ] 키포인트 → 프레임 타이밍 변환
- [ ] Unity 수신 코드 테스트
- [ ] 아바타 위치/표정/손 제어 확인
- [ ] 테스트용 샘플 영상 제작

## 🔗 참고 자료
- gloss-to-keypoint 예시 JSON
- Unity 포맷 수신 예제
- 기존 수어 아바타 프레임 정의
