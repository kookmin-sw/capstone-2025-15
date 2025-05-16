 <td align='center'> <img src="https://github.com/user-attachments/assets/6872db44-a69e-4da9-9647-199c9cbbc76e" width="100%" height="100%"></td>

## 1. 프로잭트 소개

### 프로젝트 개요

온담(溫談)은  농인을 위한 **수어 아바타 생성 서비스**입니다.
영상 속 **다중화자 음성**을 자동으로 분석하고, 각 화자의 **감정**을 인식하여 **표준 한국 수어 기반의 아바타 동작**으로 변환합니다. 농인에게도 감정과 맥락을 온전히 제공할 수 있는 서비스를 제공합니다. 

### 프로젝트 필요성

세상은 소리로 가득하지만, 누군가에겐 **보이는 손짓과 표정이 유일한 언어**입니다. 그러나 현실은 그 손짓조차 닿지 못합니다. 등록 장애인 263만 명 중, **청각·언어장애인은 45만 명**으로 **두 번째로 많지만,** **수어 방송 의무 편성률은 단 7%.** 청각장애인 **10명 중 4명은 “이해할 수 없다”는 이유로 방송 시청을 포기합니다.** 

한국 수어는 **2016년 한국수화언어법을 통해 한국어와 같은 공용어로 지정되었지만, 농인의 언어권을 보장하기엔 여전히 부족합니다.**
 <td align='center'> <img src="https://github.com/user-attachments/assets/0dbe83ca-f94f-4c1e-aa55-46cb6422eb6f" width="100%" height="100%"></td>
### 2. 소개 영상


...

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
    </tbody>
  </table>
</div>
&nbsp;  

## 3. STT 비교 및 선택
Clova Speech의 화자 분리 STT API를 활용해 화자별로 라벨링된 전사문을 추출하고,
이를 기반으로 각 화자의 발화 내용과 타임스탬프를 정확하게 분리 및 처리합니다.

또한 주요 STT 모델들에 대해 CER(Character Error Rate), 처리 시간, 예상 비용을 기준으로 성능을 비교하였고,
그 결과 CLOVA SPEECH가 가장 우수한 정확도와 속도를 보이며 최종 선정되었습니다.

### 평가 지표
CER (Character Error Rate) : 문자 단위 오류율 (낮을수록 정확)<br>
- CER = (𝑆+𝐷+𝐼) / 𝑁 <br>
S (Substitutions): 잘못된 단어로 대체된 문자의 수<br>
D (Deletions): 인식하지 못한 문자의 수<br>
I (Insertions): 잘못 삽입된 문자의 수<br>
N (Total Words): 참조(기준) 문장에 있는 총 문자의 수
<br>

처리 시간 (초) : 평균 처리 시간<br>
분당 요금 (원) : 예상 비용

| STT 시스템                                                | 평균 CER                                                | 처리 시간 (초)                                            | 예상 비용 (원)                                           |
|--------------------------------------------------------|-------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------|
| <span style="background-color:#DCFFE4"> CLOVA</span> | <span style="background-color:#DCFFE4"> 0.0836</sapn> | <span style="background-color:#DCFFE4"> 3.836</sapn> | <span style="background-color:#DCFFE4"> 16.9</sapn> |
| AWS                                                    | 0.1118                                                | 48.064                                               | 12.7                                                |
| Azure                                                  | 0.1024                                                | 47.930                                               | 16.9                                                |
| Whisper                                                | 0.1856                                                | 17.814                                               | 10.1                                                |
| Google STT                                             | 0.2031                                                | 25.361                                               | 10.1                                                |

### 후처리
STT결과값을 이용해서 각 화자에 대한 아바타를 생성하기 위해서 화자 별
전사문을 분리하였습니다.


## 4. 기술 스택
### 프론트엔드

| 역할                   | 종류                                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Programming Language | ![JavaScript](https://img.shields.io/badge/Javascript-F7DF1E?logo=javascript\&logoColor=black\&style=for-the-badge) |
| Library              | ![React](https://img.shields.io/badge/React-61DAFB?logo=react\&logoColor=black\&style=for-the-badge)                |


### 백엔드
| 역할                   | 종류                                                                                                                               |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Programming Language | ![JavaScript](https://img.shields.io/badge/Javascript-F7DF1E?logo=javascript\&logoColor=black\&style=for-the-badge)              |
| Library              | ![Express](https://img.shields.io/badge/Express-000000?logo=express\&logoColor=white\&style=for-the-badge)                       |
| Database             | ![Google Cloud Storage](https://img.shields.io/badge/GCP%20Bucket-4285F4?logo=googlecloud\&logoColor=white\&style=for-the-badge) |
| App Service          | ![Google Cloud](https://img.shields.io/badge/GCP-4285F4?logo=googlecloud\&logoColor=white\&style=for-the-badge)                  |


### AI
| 역할                   | 종류                                                                                                              |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| Programming Language | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python\&logoColor=white\&style=for-the-badge)         |
| Library              | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi\&logoColor=white\&style=for-the-badge)      |
| Application Service  | ![Google Cloud](https://img.shields.io/badge/GCP-4285F4?logo=googlecloud\&logoColor=white\&style=for-the-badge) |


### 아바타

| 역할                   | 종류                                                                                                         |
| -------------------- | ---------------------------------------------------------------------------------------------------------- |
| Programming Language | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python\&logoColor=white\&style=for-the-badge)    |
| Program              | ![Blender](https://img.shields.io/badge/Blender-F5792A?logo=blender\&logoColor=white\&style=for-the-badge) |


### 5. 기타

추가적인 내용은 자유롭게 작성하세요.
