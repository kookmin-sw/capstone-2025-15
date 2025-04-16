const axios = require('axios');
const {sttRequest} = require('../utils/gcs'); // gcs.js 파일 경로에 맞게 조정

//cloud run 호출 테스트
async function convertVideoTest() {
    const data = {
        bucket_name: 'capstone25-15',
        video_filename: 'test/947d8231-d689-45f6-ba8b-00d2a7fc4c83/originalVideo.mp4',
        wav_filename: 'test/947d8231-d689-45f6-ba8b-00d2a7fc4c83/audio.wav'
    };

    try {
        const response = await axios.post('https://convertowav-service-219454056854.asia-northeast3.run.app/convert_videos', data, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('서버 응답:', response.data);
    } catch (err) {
        console.error('에러 발생:', err.response ? err.response.data : err.message);
    }
}

//stt 테스트
async function testSTT() {
    const bucketName = 'capstone25-15';
    const audioFilePath = 'test/947d8231-d689-45f6-ba8b-00d2a7fc4c83/audio.wav';
    const outputFilePath = 'test/947d8231-d689-45f6-ba8b-00d2a7fc4c83/trans.json';
    const language = 'ko-KR';

    try {
        const result = await sttRequest(bucketName, audioFilePath, outputFilePath, language);
        console.log('✅ STT 처리 결과:', JSON.stringify(result, null, 2));
    } catch (error) {
        console.error('❌ STT 테스트 중 오류:', error.message);
    }
}

testSTT();