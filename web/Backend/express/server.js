const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.json());

//테스트 라우터 연결
const testRouter = require('./routes/test/testRouter');
app.use('/test', testRouter);

//리액트 앱 라우팅 처리
app.get(/^\/(?!api|test).*/, (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 서버 실행 중: http://localhost:${PORT}`);
});