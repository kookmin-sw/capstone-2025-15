data = [
    {
        "sentence": "딥시크의 등장으로 자극을 받은 우리 it 업계의 움직임이 빨라지고 있습니다.",
        "speaker": "1",
        "start": 0,
        "end": 5150
    },
    {
        "sentence": "은둔의 경영자로 불리는 이해진 전 네이버 의장이 복귀에 나섰고 국가대표 추격조를 만들자 독자적인 기술을 개발하자는 제안들이 쏟아지고 있습니다. 김윤미 기자의 보도입니다.",
        "speaker": "1",
        "start": 5150,
        "end": 18190
    },
    {
        "sentence": "딥시크가 밝힌 AI 모델 개발비는 80억 원 gpt4 개발비의 18분의 1, 메타 라마 3의 10분의 1에 불과합니다.",
        "speaker": "2",
        "start": 19320,
        "end": 29560
    },
    {
        "sentence": "실제 비용은 더 될 거란 추정도 나오지만 신선한 충격임은 분명합니다.",
        "speaker": "2",
        "start": 29560,
        "end": 34565
    },
    {
        "sentence": "새로운 혁신을 도모할 수 있는 충분한 가능성을 우리 산업계의 화두를 던져준 것 같습니다.",
        "speaker": "3",
        "start": 34565,
        "end": 41275
    },
    {
        "sentence": "예상을 뛰어넘은 딥시크 모델의 추론 능력에 국내 기업들의 움직임이 분주해졌습니다.",
        "speaker": "2",
        "start": 41275,
        "end": 47239
    },
    {
        "sentence": "라인야후 지분 매각 압박에도 모습을 드러내지 않던 이해진 네이버 창업자는 다음 달 7년 만에 경영으로 복귀합니다.",
        "speaker": "2",
        "start": 47239,
        "end": 55239
    },
    {
        "sentence": "AI 비전을 제시하지 못하고 있던 카카오는 오픈 AI와 손잡기로 했습니다.",
        "speaker": "2",
        "start": 55239,
        "end": 60725
    },
    {
        "sentence": "한국 기업이 개발한 AI 모델을 오픈 소스로 공개해 외부 개발자들의 활용을 독려했어야 했다는 탄식도 나왔습니다.",
        "speaker": "2",
        "start": 60725,
        "end": 68725
    },
    {
        "sentence": "한국 업체들은 구글 ms 메타만큼 막대한 개발 비용을 투자하지 못하면서 오픈 AI처럼 폐쇄적인 환경을 구축하다 보니 이도 저도 아닌 게 됐다는 겁니다.",
        "speaker": "2",
        "start": 68725,
        "end": 79905
    },
    {
        "sentence": "32b x1 무대를 만들 때 h 512장 4개월 동안",
        "speaker": "4",
        "start": 79905,
        "end": 85950
    },
    {
        "sentence": "70억 들었습니다. 좀 아쉽죠. 작년 12월에 아예 이 그룹 차원을 넘어서 글로벌 공개를 했더라면",
        "speaker": "4",
        "start": 85950,
        "end": 92884
    },
    {
        "sentence": "처음부터 소스를 공개해 누구나 활용하게 한 딥시크는 적은 돈으로 AI를 활용하려는 이용자들과 함께 자기만의 생태계를 구축할 수 있습니다.",
        "speaker": "2",
        "start": 92884,
        "end": 102755
    },
    {
        "sentence": "미국과 중국이 주도하는 경쟁에서 반격의 카드가 있을까? 사람과 자원을 한 곳으로 모아서 국가대표 AI 추격조를 만들자는 제안까지 나왔습니다.",
        "speaker": "2",
        "start": 102755,
        "end": 113205
    },
    {
        "sentence": "추격조에 선정된 회사는 한 3년 정도 한국 데이터는 다 가져다 쓰라 저작권 나중에 계산하자",
        "speaker": "5",
        "start": 113205,
        "end": 120195
    },
    {
        "sentence": "라고 아주 파격적인 데이터를 좀 열어주면 좋겠습니다.",
        "speaker": "5",
        "start": 120195,
        "end": 124450
    },
    {
        "sentence": "문제는 AI 개발의 필수인 고성능 그래픽 처리 장치 GPU를 확보하는 겁니다.",
        "speaker": "2",
        "start": 124450,
        "end": 130625
    },
    {
        "sentence": "정부는 현재 2천 장인 GPU를 2027년까지 1천만 장으로 늘리겠다고 밝혔습니다.",
        "speaker": "2",
        "start": 130625,
        "end": 136885
    },
    {
        "sentence": "전 세계에서 수요가 치솟은 GPU를 어떻게 구할지, 예산은 어떻게 마련할지, 관리 체계를 어떻게 갖출지 더 많은 과제가 따라붙었습니다.",
        "speaker": "2",
        "start": 136885,
        "end": 146190
    },
    {
        "sentence": "MBC뉴스 김윤미입니다.",
        "speaker": "2",
        "start": 146190,
        "end": 148020
    }
]

// 타임스탬프 변환 함수
function clovaTimestamping(data) {
    return {
        sentence: data.text,
        speaker: data.speaker.label,
        start: data.start,
        end: data.end
    };
}

function groupBySpeaker(data, speakerNumber) {
    const group = [];

    // 1. 그룹 배열 초기화
    for (let i = 0; i < speakerNumber; i++) {
        group.push([]);
    }

    data.forEach((datum, i) => {
        const rawSpeaker = datum.speaker;
        const numericSpeaker = parseInt(rawSpeaker, 10);


        const speakerId = (numericSpeaker - 1) % speakerNumber; // 배열 index는 0부터 시작

        group[speakerId].push({
            sentence: datum.sentence,
            start: datum.start,
            end: datum.end
        });
    });

    return group;
}

module.exports = {clovaTimestamping};