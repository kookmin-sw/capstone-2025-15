const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// 정적 파일 서빙 추가
app.use(express.static(path.join(__dirname, 'build')))
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.json());

//테스트 라우터 연결
const testRouter = require('./routes/test/testRouter');
app.use('/test', testRouter);

//파이프라인 라우터 연결
const pipelineRouter = require('./routes/pipelineRouter');
app.use('/pipeline', pipelineRouter);

//api 라우터
const videosRouter = require('./routes/api/videosRouter');
app.use('/api/videos', videosRouter);


//리액트 앱 라우팅 처리
app.get(/^\/(?!api|test).*/, (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 서버 실행 중: http://localhost:${PORT}`);
});