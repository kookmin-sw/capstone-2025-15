const axios = require('axios');
const {getSecret} = require("./gcsService");
const {clovaTimestamping, groupBySpeaker, gapPadding} = require("../utils/clovaTimestamping");

const CLOVA_API_URL = 'https://clovaspeech-gw.ncloud.com/external/v1/11266/6a0ff352edd40a4698cf042f549658cccd39feafa0875763efa41eaa99a79a72/recognizer/url';

// Naver 요청 함수 (application/json)
async function requestClova(audiourl) {
    const CLOVA_SECRET = await getSecret('CLOVA_SECRET');
    const params = {
        url: audiourl,
        language: 'ko-KR',
        completion: 'sync',
        fullText: true,
        diarization: {
            enable: true
        }
    };

    const response = await axios.post(
        CLOVA_API_URL,
        params, // 직접 객체 전달 (JSON.stringify 불필요)
        {
            headers: {
                'Content-Type': 'application/json',
                'X-CLOVASPEECH-API-KEY': CLOVA_SECRET
            }
        }
    );
    console.log(`CLOVA SPEECH 완료`);
    return response.data;
}


async function clovaSTT(audiourl, speakerCnt) {
    try {
        const sttResult = await requestClova(audiourl); //stt 요청
        console.log(sttResult);
        const timestampingResult = sttResult.segments.map(clovaTimestamping);//타임스탬프 분리, 이건 이후에 프론트에서 자막 용으로 써야함
        console.log(timestampingResult);
        const result = [];
        groupBySpeaker(timestampingResult, speakerCnt).forEach((datum) => {
            result.push(gapPadding(datum));
        })
        console.log(result);
        console.log(`✅ 타임스탬프 처리 완료`);
        return result;
    } catch (error) {
        console.error('❌ 에러 발생:', error.response?.data || error.message);
    }
}


module.exports.clovaSTT = clovaSTT;