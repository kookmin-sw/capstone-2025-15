const {v4: uuidv4} = require('uuid');
const {uploadToBucket, sttRequest} = require('../../service/gcsService');
const {Storage} = require('@google-cloud/storage');
const {korScriptGrouping} = require('../../utils/gcsSttFormatter');
const {clovaSTT} = require('../../service/clovaSpeech');
const {convertVideoToWav, signUrl} = require("../../service/gcsService");
const fs = require('fs');
const path = require('path');
const {groupBySpeaker} = require("../../utils/clovaTimestamping");

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

async function CLOVATest(req, res) {
    try {
        let result = await clovaSTT('https://storage.googleapis.com/ondam_storage/audio.wav?GoogleAccessId=fair-jigsaw-450505-q7%40appspot.gserviceaccount.com&Expires=1746458380&Signature=jkcHgUBIkuvh%2FIq9dJHxlcwo0FX7JP5fEN6pOR6kFTj7HveU9JVsWKWQ5zRgh1cc7BDVxDe0HMvc0h3QAWu97Qz9InmJ0WQZUwN%2FIA4d3Ai2UFGWFayu5DIHH%2FjSM8Ixkc9iI1LuD8qtFqV2xE7073D75pqvwW1tYQ2crq60vJfhsEwTHxvdx8AhSnN5tv9EX4KeouIG%2B74w7MULPuG4bd25ZePlIw8rZPWhMYiLfx8Yg1TwGInPNS1P1DNAzA%2FdpFTKlTtH61FSGMShULlaIhAvQIpNDNEUO57cXcAOzUSa9oREP2qBqO1B5laGVnHbGApKUlR2GdjI%2BTdBezQi7g%3D%3D');
        res.status(200).json({result: result});
    } catch (error) {
        console.error('❌ timestamp 생성 실패:', error);
        res.status(500).json({message: 'timestamp 저장 실패', error: error.message});
    }
}

async function clovapipelinetest(req, res) {
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
        let signedUrl = await signUrl(bucketName, audioPath);//음성파일 url
        let sttResult = await clovaSTT(signedUrl, 4);

        await uploadToBucket(bucketName, timestampPath, JSON.stringify(sttResult, null, 2));
        console.log(`✅ stt 완료: gs://${bucketName}/${timestampPath}`);
        return res.status(200).json({status: 'success'});
    } catch (error) {
        console.error(`❌ 처리 실패:, error`);
        return res.status(500).json({message: '처리 실패', error: error.message});
    }
}


async function localstt(req, res) {
    try {
        const uuid = '1111';
        const ext = '.mp4'
        const storage = new Storage();
        const bucketName = 'capstone25-15';
        const videoPath = `${uuid}/originalVideo${ext}`;
        const audioPath = `${uuid}/audio.wav`;
        const timestampPath = `${uuid}/timestamp.json`;
        const sttPath = `${uuid}/stt.json`;

        //wav 변환요청
        await convertVideoToWav(bucketName, videoPath, audioPath);
        console.log(`✅ wav 변환 완료: gs://${bucketName}/${audioPath}`);

        //stt, 화자분리
        let signedUrl = await signUrl(bucketName, audioPath);//음성파일 url
        let sttResult = await clovaSTT(signedUrl, 4);
        await uploadToBucket(bucketName, sttPath, JSON.stringify(sttResult[0], null, 2));
        await uploadToBucket(bucketName, timestampPath, JSON.stringify(sttResult[1], null, 2));
        console.log(`✅ stt 완료: gs://${bucketName}/${timestampPath}`);
        return res.status(200).json({status: 'success'});
    } catch (error) {
        console.error(`❌ 처리 실패:, error`);
        return res.status(500).json({message: '처리 실패', error: error.message});
    }
}

module.exports = {
    testUpload,
    testSTT,
    processTimestamp,
    CLOVATest,
    clovapipelinetest,
    localstt,
};


