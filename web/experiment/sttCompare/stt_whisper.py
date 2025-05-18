import os
from dotenv import load_dotenv
import time
import wave
from moviepy import VideoFileClip
import jiwer
import matplotlib.pyplot as plt
import pandas as pd
import requests
from pydub import AudioSegment
import json
from IPython.display import display
import re
import glob
import soundfile as sf
# STT 라이브러리 설치
from google.cloud import speech # google
import whisper # whisper
import boto3
from botocore.client import Config
import azure.cognitiveservices.speech as speechsdk
import whisper
import torch
from google.cloud import storage
# 기본 설정
load_dotenv()

p_double = re.compile(r'\(([^)]+)\)/\([^)]+\)')
p_mention = re.compile(r'@([가-힣]+)\d*')
p_slash = re.compile(r'/\(([^)]+)\)*')
p_del1 = re.compile(r'\(*')
p_del2 = re.compile(r'\)*')
p_speaker = re.compile(r'\b\d+:\s*')
p_space = re.compile(r'\s+')

# 도움 함수: 오디오 길이(초) 반환 (wave 모듈 활용)
def get_audio_duration(audio_path):
    with wave.open(audio_path, 'rb') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration
    # audio = AudioSegment.from_file(audio_path, format="mp3")
    # return len(audio) / 1000.0  # milliseconds to seconds

# WER 계산 함수 (jiwer 라이브러리 사용)
def calculate_wer(reference, hypothesis):
    # 텍스트를 소문자로 변환, 문장부호 제거, 양쪽 공백 제거 등을 적용하여 비교
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(), 
        jiwer.RemovePunctuation(), 
        jiwer.Strip(),
        jiwer.ReduceToListOfListOfWords()
    ])
    wer = jiwer.wer(reference, hypothesis, truth_transform=transformation,
                    hypothesis_transform=transformation)
    return wer

service_costs = {
    "CLOVA": 0.01,      # 네이버 CLOVA: 기본 모드 예시 (15초당 약 0.01)
    "Whisper": 0,   # OpenAI Whisper API 사용 시: 약 0.006 (분당 비용 예시)
    "Google STT": 0.006,  # Google STT: 기본 모드 시 약 0.006
    "AWS": 0.0075,      # AWS Transcribe: 기본 모드 시 약 0.0075
    "Azure": 0.01,      # Microsoft Azure Speech: 기본 모드 시 약 0.01
}

customization_capability = {
    "CLOVA": False,     # 네이버 CLOVA: 기본 모델만 제공되어 커스터마이징 지원 안 함
    "Whisper": False,   # Whisper: 공식 커스터마이징 지원 없음 (오픈소스 모델이라 직접 파인튜닝은 가능하나 별도 지원 미제공)
    "Google STT": True, # Google STT: phrase hints 등 제한적 커스터마이징 지원
    "AWS": True,        # AWS Transcribe: Custom Vocabulary 및 Custom Language Model 지원
    "Azure": True,      # Azure Speech: Custom Speech 기능 등으로 커스터마이징 지원
}

speaker_classification = {
    "CLOVA": False,
    "Whisper": False,   
    "Google STT": True, 
    "AWS": True,        
    "Azure": True, 
}

def clean_line(line: str) -> str:
    # 1) 이중 괄호 표기: (A)/(B) → A  
    line = p_double.sub(r'\1', line)
    # 2) 멘션 삭제: @이름10 등
    line = p_mention.sub(r'\1', line)
    # 3) /(?) 제거: "/(idiom)" → ""
    line = p_slash.sub('', line)
    # 괄호 삭제
    line = p_del1.sub('', line)
    line = p_del2.sub('', line)
    # 4) 화자 번호 삭제: "4:" or "10:" etc.
    line = p_speaker.sub('', line)
    # 6) 중복 공백→한 칸
    line = p_space.sub(' ', line).strip()
    return line


def clean_text(infile: str, outfile: str):
    infile = "text.txt"
    outfile = "text.txt"

    with open(infile, 'r', encoding='utf-8') as fin:
        raws = [line.rstrip('\n') for line in fin if line.strip()]
    rst = []
    for s in raws:
        out = clean_line(s)
        if out:
            rst.append(out + '\n')
            print(out)
    with open(outfile, 'w', encoding='utf-8') as fout:
        fout.writelines(rst)
def stt_whisper(audio_path):
    # 2) 오디오 파일을 모델에 전달하여 transcription 수행
    result = whisper_model.transcribe(audio_path, language="ko")

    # 3) 텍스트 결과 추출
    transcript = result.get("text", "").strip()

    print("whisper complete")

    return transcript
def process_one_gpu(audio_dir, script_dir, basename, engine):
    """
    audio_dir: .wav 파일 폴더
    script_dir: 정답 스크립트(.txt) 폴더
    json_dir: 메타데이터 폴더
    basename: 확장자 제외 공통 파일명
    engine: STT_FUNCTIONS 키
    """
    t0 = time.time()

    # 1) 메타데이터(domain) 로드
    domain = os.path.basename(script_dir)

    # 2) 정답 스크립트(ground-truth) GPU 전처리
    txt_path = os.path.join(script_dir, f"{basename}.txt")
    with open(txt_path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    # 3) STT 호출
    audio_path = os.path.join(audio_dir, f"{basename}.wav")
    try:
        data, sr = sf.read(audio_path)
        duration_sec = len(data) / sr
    except Exception:
        duration_sec = 0

    #stt_func = STT_FUNCTIONS[engine]
    t1 = time.time()
    hypothesis = stt_whisper(audio_path)               # 문자열 전체
    proc_time = time.time() - t1

    # 4) STT 결과 GPU 전처리
    # 하나로 합친 뒤 WER
    ref = " ".join(lines)
    hyp_txt = hypothesis.replace('\n', ' ')
    file_wer = calculate_wer(ref, hyp_txt)

    # 5) 비용 계산 (분당)
    cost = service_costs.get(engine, 0.0)
    cost_usd = round((duration_sec/60.0)*cost, 4)

    total_time = time.time() - t0

    return {
        'basename':      basename,
        'domain':        domain,
        'engine':        engine,
        'duration_sec':  round(duration_sec, 3),
        'wer':           round(file_wer, 3),
        'stt_time_sec':  round(proc_time, 3),
        'total_time_sec': round(total_time, 3),
        'cost_usd':      cost_usd,
        'transcript' : hypothesis
    }



if torch.cuda.is_available() :
    print("cuda" )
else :
    print("cpu")
print(torch.version.cuda)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
whisper_model = whisper.load_model("medium", device=device)
print("whisepr model")
root_audio_dir = './VS1/data'
root_script_dir = './VS1/data'
domains = [
    d for d in os.listdir(root_script_dir)
    if os.path.isdir(os.path.join(root_script_dir, d))
]
print(domains)
whisper_results = []

for domain in domains:
    script_dir = os.path.join(root_script_dir, domain)
    audio_dir = os.path.join(root_audio_dir, domain)

    basenames = [
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(script_dir, '*.txt'))
    ]

    for b in basenames:
        # process_one_gpu 대신 process_one_serial 같은 함수로 대체하거나
        # process_one_gpu를 순차 호출(내부에서 GPU를 한 번에 하나만 쓰게 처리해야 함)
        
        result = process_one_gpu(audio_dir, script_dir, b, "Whisper")
        whisper_results.append(result)

 # 6) cudf DataFrame + 집계
gdf = pd.DataFrame(whisper_results)

    # 8) 파일별 전사결과도 별도 CSV로
gdf.to_csv(
        'stt_whisper_results_medium.csv', index=False, encoding='utf-8-sig'
    )
print("✅ stt_whisper_results.csv 저장 완료")