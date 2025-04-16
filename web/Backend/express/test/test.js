const axios = require('axios');

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

convertVideoTest();
