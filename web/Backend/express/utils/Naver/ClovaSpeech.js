const axios = require('axios');
const {getSecret} = require("../gcs");


const CLOVA_API_URL = 'https://clovaspeech-gw.ncloud.com/external/v1/11266/6a0ff352edd40a4698cf042f549658cccd39feafa0875763efa41eaa99a79a72/recognizer/url';

// Naver 요청 함수 (application/json)
async function requestClovaUpload(audiourl) {
    const CLOVA_SECRET = getSecret('CLOVA_SECRET');
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
