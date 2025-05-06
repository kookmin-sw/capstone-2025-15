// utils/gcsService.js
const {Storage} = require('@google-cloud/storage');
const {SpeechClient} = require('@google-cloud/speech');
const {SecretManagerServiceClient} = require('@google-cloud/secret-manager');
const axios = require("axios");

// GCS 업로드
async function uploadToBucket(bucketName, filePath, file) {
    const storage = new Storage();
    try {
        await storage.bucket(bucketName).file(filePath).save(file);
        console.log(`✅ GCS 업로드 완료: gs://${bucketName}/${filePath}`);
    } catch (error) {
        console.error('❌ GCS 업로드 실패:', error);
        throw error;
    }
}

// STT
async function sttRequest(bucketName, audioFilePath, outputFilePath, language = 'ko-KR') {
    const speechClient = new SpeechClient();
    const audioUri = `gs://${bucketName}/${audioFilePath}`;

    const config = {
        encoding: 'LINEAR16',
        sampleRateHertz: 44100,
        languageCode: language,
        enableWordTimeOffsets: true,
        enableAutomaticPunctuation: true,
        useEnhanced: true,
        model: 'latest_long',
    };

    try {
        console.log(`🎙 STT 요청 시작: ${audioUri}`);
        const [operation] = await speechClient.longRunningRecognize({config, audio: {uri: audioUri}});
        const [response] = await operation.promise();

        if (!response?.results?.length) {
            throw new Error('No transcription results found');
        }

        const transcriptionData = response.results.map(result => ({
            text: result.alternatives[0].transcript,
            words: result.alternatives[0].words.map(wordInfo => ({
                word: wordInfo.word,
                startTime: parseFloat(wordInfo.startTime?.seconds || 0) + (wordInfo.startTime?.nanos || 0) * 1e-9,
                endTime: parseFloat(wordInfo.endTime?.seconds || 0) + (wordInfo.endTime?.nanos || 0) * 1e-9,
            })),
        }));

        await uploadToBucket(bucketName, outputFilePath, JSON.stringify(transcriptionData, null, 2));
        console.log(`✅ STT 결과 저장 완료: gs://${bucketName}/${outputFilePath}`);

        return transcriptionData;
    } catch (error) {
        console.error('❌ STT 요청 오류:', error);
        throw error;
    }
}

//  Secret 가져오기
async function getSecret(SECRET_ID) {
    const client = new SecretManagerServiceClient();
    const [version] = await client.accessSecretVersion({
        name: `projects/219454056854/secrets/${SECRET_ID}/versions/latest`,
    });
    return version.payload.data.toString('utf8');
}

async function convertVideoToWav(bucketName, videoPath, wavPath) {
    const convertowavServiceUrl = 'https://convertowav-service-219454056854.asia-northeast3.run.app/convert_videos'
    const data = {
        bucket_name: bucketName,
        video_filename: videoPath,
        wav_filename: wavPath,
    };

    try {
        const response = await axios.post(convertowavServiceUrl, data, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.error('wav 변환 완료');
    } catch (err) {
        console.error('에러 발생:', err.response ? err.response.data : err.message);
    }
}

module.exports = {
    uploadToBucket,
    sttRequest,
    getSecret,
    convertVideoToWav,
};
