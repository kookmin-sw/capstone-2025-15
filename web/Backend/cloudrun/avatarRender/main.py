from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
import os, uuid, json, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
# from google.cloud import storage  # GCS 관련 부분은 주석 처리
from urllib.parse import urlparse

app = FastAPI()

KEYPOINT_DIR = "keypoints"
OUTPUT_DIR = "output"
BLEND_FILE = "female01_8_2.blend"
CHUNKS = 6

os.makedirs(KEYPOINT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ✅ GCS 업로드 함수 (로컬로 저장하는 방식으로 변경)
# def upload_to_gcs(local_path: str, gcs_uri: str):
#     parsed = urlparse(gcs_uri)
#     assert parsed.scheme == "gs", "❌ 잘못된 GCS URI입니다."

#     bucket_name = parsed.netloc
#     blob_path = parsed.path.lstrip("/")

#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(blob_path)
#     blob.upload_from_filename(local_path)

#     print(f"✅ GCS 업로드 완료: gs://{bucket_name}/{blob_path}")
#     return f"gs://{bucket_name}/{blob_path}"

# 애니메이션 생성 함수
def generate_animation(json_path, start_frame, end_frame):
    # Blender 애니메이션 생성
    result = subprocess.run([
        "blender", "--factory-startup", "-b", "female01_8.blend", "-P", "generate_animation.py", "--",
        json_path, str(start_frame), str(end_frame)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"❌ 애니메이션 생성 실패: {json_path}")
        print(result.stdout.decode())
        print(result.stderr.decode())
        raise RuntimeError("애니메이션 생성 실패")
    else:
        print(f"✅ 애니메이션 생성 성공: {json_path}")

# 렌더링 함수
def render_animation(json_path, start_frame, end_frame, output_path):
    # 렌더링 작업
    result = subprocess.run([
        "blender", "--factory-startup", "-b", "female01_8.blend", "-P", "render_chunk.py", "--",
        json_path, str(start_frame), str(end_frame), output_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"❌ 렌더 실패: {output_path}")
        print(result.stdout.decode())
        print(result.stderr.decode())
        raise RuntimeError("렌더링 실패")
    else:
        print(f"✅ 렌더 성공: {output_path}")

@app.post("/render/parallel")
async def render_parallel(file: UploadFile = File(...), bucket: str = Form(...)):
    uid = str(uuid.uuid4())
    json_path = f"{KEYPOINT_DIR}/{uid}.json"
    output_dir = f"{OUTPUT_DIR}/{uid}"
    os.makedirs(output_dir, exist_ok=True)

    # 업로드된 JSON 저장
    with open(json_path, "wb") as f:
        f.write(await file.read())

    # JSON 로드 및 프레임 수 계산
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    total_frames = len(data)
    chunk_size = total_frames // CHUNKS

    # 애니메이션 생성
    try:
        generate_animation(json_path, 0, total_frames - 1)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"애니메이션 생성 실패: {str(e)}"})

    # 렌더링 함수
    def render_chunk(i):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < CHUNKS - 1 else total_frames
        output_file = os.path.join(output_dir, f"output_{i}.mp4")

        result = subprocess.run([
            "blender", "--factory-startup", "-b", BLEND_FILE, "-P", "render_chunk.py", "--",
            json_path, str(start), str(end - 1), output_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0 or not os.path.exists(output_file):
            print(f"❌ 렌더 실패 {i}: {output_file}")
            print(result.stdout.decode())
            print(result.stderr.decode())
        else:
            print(f"✅ 렌더 성공 {i}: {output_file}")
        return output_file

    # 병렬 실행
    output_files = list(ThreadPoolExecutor(max_workers=CHUNKS).map(render_chunk, range(CHUNKS)))

    # 병합 대상 필터링
    valid_parts = [f for f in output_files if os.path.exists(f) and os.path.getsize(f) > 0]

    if not valid_parts:
        return JSONResponse(status_code=500, content={"error": "렌더링된 mp4 파일이 없습니다."})

    # list.txt 작성
    list_path = os.path.join(output_dir, "list.txt")
    with open(list_path, "w") as f:
        for path in valid_parts:
            f.write(f"file '{os.path.basename(path)}'\n")

    # 병합 실행
    final_output = os.path.join(output_dir, "final_output.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt",
        "-c", "copy", "final_output.mp4"
    ], cwd=output_dir)

    if not os.path.exists(final_output):
        return JSONResponse(status_code=500, content={"error": "final_output.mp4 생성 실패"})

    # 로컬에 결과물 저장
    local_file_path = final_output

    # 로컬 결과물 삭제 (선택사항)
    shutil.rmtree(output_dir)
    os.remove(json_path)

    return FileResponse(local_file_path, media_type="video/mp4", filename="rendered.mp4")

