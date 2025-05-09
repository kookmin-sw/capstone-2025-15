// 타임스탬프 변환 함수
function clovaTimestamping(data) {
    return {
        sentence: data.text,
        speaker: data.speaker.label,
        start: data.start,
        end: data.end
    };
}

module.exports = {clovaTimestamping};