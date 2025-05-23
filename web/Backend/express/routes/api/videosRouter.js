const express = require('express');
const {Storage} = require('@google-cloud/storage');

const router = express.Router();

// GCS 설정
const storage = new Storage();
const bucketName = 'capstone25-15-fe';
const prefix = 'demonstrationData/videos/';

router.get('/', async (req, res) => {
    try {
        console.log("📡 GCS 파일 요청 시작...");
        const [files] = await storage.bucket(bucketName).getFiles({prefix});

        console.log("📁 가져온 파일 수:", files.length);
        // 폴더 추출 (GCS에서는 디렉토리도 파일처럼 다뤄짐)
        const folders = new Set();
        files.forEach(file => {
            const parts = file.name.split('/');
            if (parts.length >= 4) {
                folders.add(parts[2]); // demonstrationData/videos/1/
            }
        });

        // 정렬 및 응답
        const folderList = Array.from(folders).sort().map(folder => {
            const base = `https://storage.googleapis.com/${bucketName}/${prefix}${folder}`;
            return {
                id: folder,
                title: `영상 ${folder}`,
                thumbnail: `${base}/thumb1.png`,
                videoUrl: `${base}/main.mp4`,
                avatarData: [
                    {speaker: 1, videoUrl: `${base}/avatar1.mp4`},
                    {speaker: 2, videoUrl: `${base}/avatar2.mp4`},
                    {speaker: 3, videoUrl: `${base}/avatar3.mp4`},
                    {speaker: 4, videoUrl: `${base}/avatar4.mp4`}
                ],
                subtitleUrl: `${base}/timestamp.json`
            };
        });

        res.json(folderList);
    } catch (err) {
        console.error('🔥 GCS 목록 조회 오류:', err);
        res.status(500).json({error: '영상 목록을 불러오지 못했습니다.'});
    }
});

module.exports = router;