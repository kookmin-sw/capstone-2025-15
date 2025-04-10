const {v4: uuidv4} = require('uuid');
const {uploadToBucket} = require('../../utils/gcs');

const bucketName = 'capstone25-15'; // 실제 GCP 버킷 이름으로 변경

async function testUpload(req, res) {
    try {
        if (!req.file) {
            return res.status(400).json({message: '파일이 없습니다.'});
        }

        const uuid = uuidv4();
        const ext = req.file.originalname.split('.').pop();
        const gcsPath = `test/${uuid}/originalVideo.${ext}`;

        await uploadToBucket(bucketName, gcsPath, req.file.buffer);

        console.log(`업로드 완료: gs://${bucketName}/${gcsPath}`);

        return res.status(200).json({
            message: '업로드 성공',
            gcsUrl: `gs://${bucketName}/${gcsPath}`,
            uuid,
        });
    } catch (error) {
        console.error('업로드 실패:', error);
        return res.status(500).json({message: '업로드 실패', error: error.message});
    }
}

module.exports = {testUpload};