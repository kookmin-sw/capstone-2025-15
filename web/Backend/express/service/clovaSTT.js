const {requestClova} = require('../utils/Naver/ClovaSpeech');

// 타임스탬프 변환 함수
function timestamping(data) {
    return {
        sentence: data.text,
        speaker: data.speaker.label,
        start: data.start,
        end: data.end
    };
}


async function clovaSTT(audiourl) {
    try {
        const sttresult = await requestClova(audiourl); //stt 요청
        const result = sttresult.segments.map(timestamping);//타임스탬프 분리
        console.log(`✅ 타임스탬프 처리 완료`);
        return result;
    } catch (error) {
        console.error('❌ 에러 발생:', error.response?.data || error.message);
    }
}

module.exports = {clovaSTT};