const {v4: uuidv4} = require("uuid");
const path = require("path");
const {uploadToBucket, convertVideoToWav} = require("../service/gcsService");
const {Storage} = require("@google-cloud/storage");
const {clovaSTT} = require("../service/clovaSpeech");

async function pipeline(res, req) {
    try {
        if (!req.file) return res.status(400).json({message: '파일이 없습니다.'});
        const uuid = uuidv4();
        const ext = path.extname(req.file.originalname);
        const storage = new Storage();
        const bucketName = 'capstone25-15';
        const videoPath = `${uuid}/originalVideo${ext}`;
        const audioPath = `${uuid}/audio.wav`;
        const timestampPath = `${uuid}/timestamp.json`;

        console.log(`✅ 처리시작: ${uuid}`);
        //영상 업로드
        await uploadToBucket(bucketName, videoPath, req.file.buffer);
        console.log(`✅ 업로드 완료: gs://${bucketName}/${videoPath}`);

        //wav 변환요청
        await convertVideoToWav(bucketName, videoPath, audioPath);
        console.log(`✅ wav 변환 완료: gs://${bucketName}/${audioPath}`);

        //stt, 화자분리
        let sttResult = await clovaSTT(audioPath);
        await uploadToBucket(bucketName, timestampPath, JSON.stringify(sttResult, null, 2));
        console.log(`✅ stt 완료: gs://${bucketName}/${timestampPath}`);
    } catch (error) {
        console.error(`❌ 처리 실패:`, error);
        return res.status(500).json({message: '처리 실패', error: error.message});
    }
}