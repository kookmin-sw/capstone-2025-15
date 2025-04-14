// routes/test/testRouter.js
const express = require('express');
const multer = require('multer');
const {testUpload} = require('../../controller/test/testController');

const router = express.Router();
const upload = multer({storage: multer.memoryStorage()});

// ✅ GET /test → 업로드 폼 페이지 렌더링
router.get('/', (req, res) => {
    res.render('test/index');  // views/test/index.ejs
});

// ✅ POST /test/upload → 파일 업로드 처리
router.post('/upload', upload.single('video'), testUpload);

module.exports = router;
