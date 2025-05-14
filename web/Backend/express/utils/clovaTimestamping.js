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
    group.forEach(datum => {
        if (datum.length == 0) {
            datum.push({
                sentence: "",
                start: 0,
                end: 0,
            });
        }
    })

    return group;
}

function gapPadding(data) {
    const padded = [];

    // 맨 앞에 빈 공백 삽입 필요 시
    if (data[0].start > 0) {
        padded.push({
            sentence: "",
            start: 0,
            end: data[0].start
        });
    }

    // 첫 문장 추가
    padded.push(data[0]);

    for (let i = 1; i < data.length; i++) {
        const prev = data[i - 1];
        const curr = data[i];

        // ✅ 이전 발화와 현재 발화 사이에 실제 gap이 있는 경우에만 공백 추가
        if (curr.start > prev.end) {
            padded.push({
                sentence: "",
                start: prev.end,
                end: curr.start
            });
        }

        padded.push(curr);
    }

    return padded;
}


//빈 배열 (화자가 4보다 작은 경우 나오는 빈 배열에 대해 함수 적용시 문제 -> 빈 배열은 더미 데이터 1개씩 넣어주기
module.exports = {clovaTimestamping, groupBySpeaker, gapPadding};