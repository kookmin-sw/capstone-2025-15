from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import asyncio
import logging
from google.cloud import storage
import ffmpeg
import os

PORT = int(os.environ.get("PORT", 8080))
CMD = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(PORT)]
app = FastAPI()

# 로그 설정
logging.basicConfig(level=logging.INFO)

# wav파일로 변환
async def convert_video_to_wav(input_video_path, output_wav_path):
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: ffmpeg.input(input_video_path).output(output_wav_path, ac=1).run())
        logging.info(f"Converted video {input_video_path} to {output_wav_path}")
    except Exception as e:
        logging.error(f"FFmpeg conversion failed for {input_video_path}: {str(e)}", exc_info=True)
        raise Exception(f"FFmpeg conversion failed: {str(e)}")

# 동영상 다운로드
async def download_video_from_bucket(bucket_name, video_filename, local_video_filename):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(video_filename)
        blob.download_to_filename(local_video_filename)
        logging.info(f"Downloaded {video_filename} from {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to download {video_filename} from {bucket_name}: {str(e)}", exc_info=True)
        raise Exception(f"Failed to download {video_filename}: {str(e)}")

# WAV 파일 업로드
async def upload_wav_to_bucket(bucket_name, wav_filename, destination_filename):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_filename)
        blob.upload_from_filename(wav_filename)
        logging.info(f"Uploaded {destination_filename} to {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to upload {destination_filename} to {bucket_name}: {str(e)}", exc_info=True)
        raise Exception(f"Failed to upload {destination_filename}: {str(e)}")

# 요청 처리
async def process_video(bucket_name, video_filename, wav_filename):
    local_video_path = f"/tmp/{video_filename.split('/')[-1]}"
    local_wav_path = f"/tmp/{wav_filename.split('/')[-1]}"

    try:
        # 동영상 다운로드
        await download_video_from_bucket(bucket_name, video_filename, local_video_path)

        # 동영상을 WAV로 변환
        await convert_video_to_wav(local_video_path, local_wav_path)

        # WAV 파일 업로드
        await upload_wav_to_bucket(bucket_name, local_wav_path, wav_filename)

        # 로컬 파일 삭제
        os.remove(local_video_path)
        os.remove(local_wav_path)

        return {"video": video_filename, "status": "success"}

    except Exception as e:
        logging.error(f"Error processing {video_filename}: {str(e)}", exc_info=True)
        return {"video": video_filename, "status": "failed", "error": str(e)}

# 입력 데이터 모델
class VideoRequest(BaseModel):
    bucket_name: str
    video_filename: str  # 하나의 동영상 파일명만 받도록 수정
    wav_filename: str  # 저장할 WAV 파일명을 요청받기

# API 엔드포인트
@app.post("/convert_videos")
async def convert_videos(request: VideoRequest):
    # 비동기 작업 처리
    try:

        result = await process_video(request.bucket_name, request.video_filename, request.wav_filename)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}