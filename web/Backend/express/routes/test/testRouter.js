// routes/test/testRouter.js
const express = require('express');
const multer = require('multer');
const {testUpload, testSTT, processTimestamp} = require('../../controller/test/testController');

const router = express.Router();
const upload = multer({storage: multer.memoryStorage()});

// ✅ GET /test → 업로드 폼 페이지 렌더링
router.get('/', (req, res) => {
    res.render('test/index');  // views/test/index.ejs
});

// ✅ POST /test/upload → 파일 업로드 처리
router.post('/upload', upload.single('video'), testUpload);

//stt 업로드 테스트
router.get('/stt', testSTT);

// ✅ 후처리 (timestamp 생성)
router.get('/timestamp', processTimestamp);

module.exports = router;
