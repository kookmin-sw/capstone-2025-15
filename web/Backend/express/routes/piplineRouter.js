const {pipeline} = require('../../controller/pipeline');
router.post('/upload', upload.single('video'), pipeline);
