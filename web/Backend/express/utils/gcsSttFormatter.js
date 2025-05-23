// 문장 부호 기준으로 문장 나누기 (. , ! ?)
function korSentenceSplitter(text) {
    const raw = text.split(/([.?!,])/).filter(Boolean);
    const sentences = [];
    for (let i = 0; i < raw.length; i += 2) {
        let sentence = raw[i] + (raw[i + 1] || '');
        sentences.push(sentence.trim());
    }
    return sentences;
}

// 단일 문장에 대한 시작/끝 타임스탬프 추출
function korExtractTimestamp(sentence, words, startIndex) {
    let index = startIndex;
    let cleaned = sentence.replace(/\s+/g, '');
    let built = '';
    let start = null;

    while (index < words.length) {
        const wordObj = words[index];
        if (!wordObj?.word) break;

        const word = wordObj.word.replace(/^▁/, '');
        if (!start) start = parseFloat(wordObj.startTime);

        built += word;
        index++;

        if (built.length >= cleaned.length) break;
    }

    const end = parseFloat(words[Math.max(index - 1, 0)].endTime);
    return {
        text: sentence,
        start,
        end,
        nextIndex: index
    };
}

// 단일 script 객체 처리
function korProcessScript(script) {
    const {text, words} = script;
    const sentences = korSentenceSplitter(text);
    const result = [];

    let index = 0;
    for (const sentence of sentences) {
        while (words[index]?.word === '▁') index++; // 앞쪽 공백 제거

        const ts = korExtractTimestamp(sentence, words, index);
        result.push({text: ts.text, start: ts.start, end: ts.end});
        index = ts.nextIndex;

        while (words[index]?.word === '▁') index++; // 뒷쪽 공백 제거
    }

    return result;
}

// 전체 script 배열 처리
function korScriptGrouping(scripts) {
    return scripts.map(korProcessScript);
}

module.exports = {
    korScriptGrouping,
    korSentenceSplitter,
    korExtractTimestamp,
    korProcessScript,
};
