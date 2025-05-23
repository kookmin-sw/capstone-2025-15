# linuxserver/blender 이미지를 사용
FROM linuxserver/blender:4.0.2

# 필수 패키지 설치 (ffmpeg, python3-pip 등)
RUN apt-get update && apt-get install -y ffmpeg \
    && apt-get install -y python3-pip \
    && apt-get clean

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일을 작업 디렉토리로 복사
COPY requirements.txt /app/requirements.txt

# 의존성 설치
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# FastAPI 애플리케이션 코드 복사
COPY . /app/

# Cloud Run에서 사용할 포트 지정
EXPOSE 8080

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
