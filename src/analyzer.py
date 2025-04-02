import MeCab  # ✅ 꼭 필요!

tagger = MeCab.Tagger(
    '-d /opt/homebrew/lib/mecab/dic/mecab-ko-dic -r /opt/homebrew/etc/mecabrc'
)

def analyze(sentence: str) -> list:
    lines = tagger.parse(sentence).split("\n")
    words = []
    for line in lines:
        if line == "EOS" or line == "":
            continue
        token, feature = line.split("\t")[0], line.split("\t")[1]
        pos = feature.split(",")[0]
        if pos not in ["JKS", "JKB", "JX", "EF", "EC", "SF"]:
            words.append(token)
    return words


