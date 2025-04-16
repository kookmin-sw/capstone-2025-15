// utils/gcs.js
const {Storage} = require('@google-cloud/storage');
const {SpeechClient} = require('@google-cloud/speech');

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

module.exports = {
    uploadToBucket,
    sttRequest,
};
