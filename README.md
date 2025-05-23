<td align='center'> <img src="https://github.com/user-attachments/assets/6872db44-a69e-4da9-9647-199c9cbbc76e" width="100%" height="100%"></td>

<td align='center'> <img src="https://github.com/user-attachments/assets/ec00a1e1-21e2-4fd4-9cb2-a567efd7d41e" width="100%" height="100%"></td>

- - -

## 1. 프로젝트 소개

### 프로젝트 개요

온담(溫談)은 농인을 위한 **수어 아바타 생성 서비스**입니다.  
영상 속 **다중화자 음성**을 자동으로 분석하고, 각 화자의 **감정**을 인식하여 **표준 한국 수어 기반의 아바타 동작**으로 변환합니다.  
농인에게도 감정과 맥락을 온전히 제공할 수 있는 서비스를 제공합니다.

### 프로젝트 필요성

세상은 소리로 가득하지만, 누군가에겐 **보이는 손짓과 표정이 유일한 언어**입니다. 그러나 현실은 그 손짓조차 닿지 못합니다.  
등록 장애인 263만 명 중, **청각·언어장애인은 45만 명**으로 **두 번째로 많지만**,  
**수어 방송 의무 편성률은 단 7%.**  
청각장애인 **10명 중 4명은 “이해할 수 없다”는 이유로 방송 시청을 포기합니다.**  
한국 수어는**2016년 한국수화언어법을 통해 한국어와 같은 공용어로 지정되었지만, 농인의 언어권을 보장하기엔 여전히 부족합니다.**

<td align='center'> <img src="https://github.com/user-attachments/assets/0dbe83ca-f94f-4c1e-aa55-46cb6422eb6f" width="100%" height="100%"></td>

### 2. 소개 영상

(여기에 영상 링크나 썸네일을 넣어주세요)

---

## 2. 팀 소개

<div align='center'>
  <table>
    <tbody>
      <tr>
        <td align='center'><a href="https://github.com/ddugel3"><img src="https://avatars.githubusercontent.com/u/56158371?v=4" width="100" height="100"></td>
        <td align='center'><a href="https://github.com/govl0407"><img src="https://avatars.githubusercontent.com/u/62105026?v=4" width="100" height="100"></td>
        <td align='center'><a href="https://github.com/GiyeonYang"><img src="https://github.com/user-attachments/assets/4a4a3eeb-0da1-4279-854f-051be87b53ca" width="100" height="100"></td>
      </tr>
      <tr>
        <td align='center'>20203059</td>
        <td align='center'>20203103</td>
        <td align='center'>20203150</td>
      </tr>
      <tr>
        <td align='center'>최건웅</td>
        <td align='center'>최정민</td>
        <td align='center'>양기연</td>
      </tr>
      <tr>
        <td align='center'>팀장, 수어 문법 변환 및 감정 분석</td>
        <td align='center'>웹 개발 및 STT 분석</td>
        <td align='center'>아바타 생성</td>
      </tr>
    </tbody>
  </table>
</div>
&nbsp;  

---

## 주요 기술

### 1. STT 비교 및 선택

AI-Hub 공개 주요 영역별 회의 음성인식 데이터 50개 음성데이터 약 50시간 음성에 대한 비교 분석 결과  
https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=464

| 엔진         | CER    | 비용     | 처리 시간 (초) |
|------------|--------|--------|-----------|
| AWS        | 0.2165 | 0.3723 | 194.00    |
| Azure      | 0.2147 | 0.4964 | 1463.50   |
| CLOVA      | 0.2111 | 0.4964 | 25.40     |
| Google STT | 0.3756 | 0.2979 | 533.41    |
| Whisper    | 0.2663 | 0.0000 | 225.25    |

<td align='center'> <img width="882" alt="Image" src="https://github.com/user-attachments/assets/7b4808d2-48a5-41b5-a916-c5f7334998d1" /></td>

### 평가 지표

CER (Character Error Rate): 문자 단위 오류율 (낮을수록 정확)

- CER = (𝑆+𝐷+𝐼) / 𝑁
    - S (Substitutions): 잘못된 단어로 대체된 문자 수
    - D (Deletions): 인식하지 못한 문자 수
    - I (Insertions): 잘못 삽입된 문자 수
    - N (Total Words): 기준 문장의 총 문자 수

---

## 4. 기술 스택

### 🖥️ Frontend

<img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=React&logoColor=black">

### 🛠️ Backend

<img src="https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=Express&logoColor=white"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white"><img src="https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=Google%20Cloud&logoColor=white">

### 🧍 Avatar

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"><img src="https://img.shields.io/badge/Blender-F5792A?style=for-the-badge&logo=Blender&logoColor=white">

### 🧠 KSL / Sentiment Analysis

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"><img src="https://img.shields.io/badge/Huggingface-FFAA00?style=for-the-badge&logo=HuggingFace&logoColor=white"><img src="https://img.shields.io/badge/KcELECTRA-orange?style=for-the-badge&logo=github&logoColor=white"><img src="https://img.shields.io/badge/Kiwi-blue?style=for-the-badge&logo=KoNLPy&logoColor=white"><img src="https://img.shields.io/badge/MeCab-green?style=for-the-badge&logo=KoNLPy&logoColor=white">

---

## 5. 기타

추가적인 내용은 자유롭게 작성하세요.
