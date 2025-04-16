const {v4: uuidv4} = require('uuid');
const {uploadToBucket, sttRequest} = require('../../utils/gcs');
const {Storage} = require('@google-cloud/storage');
const {korScriptGrouping} = require('../../utils/sttFormatter');
const fs = require('fs');
const path = require('path');

const storage = new Storage();
const bucketName = 'capstone25-15';

// ✅ 업로드
async function testUpload(req, res) {
    try {
        if (!req.file) return res.status(400).json({message: '파일이 없습니다.'});

        const uuid = uuidv4();
        const ext = path.extname(req.file.originalname);
        const gcsPath = `test/${uuid}/originalVideo${ext}`;

        await uploadToBucket(bucketName, gcsPath, req.file.buffer);
        console.log(`✅ 업로드 완료: gs://${bucketName}/${gcsPath}`);

        return res.status(200).json({
            message: '업로드 성공',
            gcsUrl: `gs://${bucketName}/${gcsPath}`,
            uuid,
        });
    } catch (error) {
        console.error('❌ 업로드 실패:', error);
        return res.status(500).json({message: '업로드 실패', error: error.message});
    }
}

// ✅ STT만 처리 (trans.json 생성)
async function testSTT(req, res) {
    const uuid = '947d8231-d689-45f6-ba8b-00d2a7fc4c83'; // 추후 req.query.uuid로 변경 가능
    const audioFilePath = `test/${uuid}/audio.wav`;
    const transcriptPath = `test/${uuid}/trans.json`;
    const language = 'ko-KR';

    try {
        const result = await sttRequest(bucketName, audioFilePath, transcriptPath, language);
        console.log('✅ STT 완료');
        res.status(200).json({message: '✅ STT 완료', transcriptPath, result});
    } catch (error) {
        console.error('❌ STT 실패:', error);
        res.status(500).json({message: 'STT 실패', error: error.message});
    }
}

// ✅ 후처리만 별도 수행 (trans → timestamp.json 저장)
async function processTimestamp(req, res) {
    const uuid = '947d8231-d689-45f6-ba8b-00d2a7fc4c83'; // 추후 req.query.uuid 사용 가능
    const transcriptPath = `test/${uuid}/trans.json`;
    const timestampPath = `test/${uuid}/timestamp.json`;
    const localTranscript = `/tmp/${uuid}_trans.json`;
    const localTimestamp = `/tmp/${uuid}_timestamp.json`;

    try {
        // 1. trans.json 다운로드
        await storage.bucket(bucketName).file(transcriptPath).download({destination: localTranscript});

        // 2. 후처리
        const raw = JSON.parse(fs.readFileSync(localTranscript, 'utf-8'));
        const result = korScriptGrouping(raw);
        fs.writeFileSync(localTimestamp, JSON.stringify(result, null, 2), 'utf-8');

        // 3. 업로드
        await storage.bucket(bucketName).upload(localTimestamp, {
            destination: timestampPath,
        });

        res.status(200).json({
            message: '✅ 후처리 및 timestamp 저장 완료',
            path: `gs://${bucketName}/${timestampPath}`,
            data: result,
        });
    } catch (error) {
        console.error('❌ timestamp 생성 실패:', error);
        res.status(500).json({message: 'timestamp 저장 실패', error: error.message});
    }
}

module.exports = {
    testUpload,
    testSTT,
    processTimestamp
};
