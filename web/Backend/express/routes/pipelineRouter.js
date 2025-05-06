const {pipeline} = require('../controller/pipelineController');

const multer = require('multer');
const express = require("express");

const router = express.Router();
const upload = multer({storage: multer.memoryStorage()});
router.post('/upload', upload.single('video'), pipeline);
module.exports = router;