from typing import List

def recombine_tokens(tokens: List[str]) -> List[str]:

    result = []
    buffer = []

    for token in tokens:
        buffer.append(token)
        joined = "".join(buffer)

        # 의미 단위 사전 기반 병합 후보 예시 (향후 외부 사전으로 확장 가능)
        if joined in {"걸리다", "가고싶다", "잃어버리다", "돌아가다", "받아들이다"}:
            result.append(joined)
            buffer = []
        elif len(buffer) >= 3:  # 병합 실패 시 앞 토큰부터 결과로 내보냄
            result.append(buffer[0])
            buffer = buffer[1:]

    # 버퍼에 남은 토큰 처리
    result.extend(buffer)

    return result
