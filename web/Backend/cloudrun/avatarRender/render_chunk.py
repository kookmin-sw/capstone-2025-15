import bpy
import json
import sys
from mathutils import Vector, Quaternion

# CLI 인자 받기
json_path = sys.argv[-4]
start_frame = int(sys.argv[-3])
end_frame = int(sys.argv[-2])
output_path = sys.argv[-1]

# Blender 렌더링 설정
scene = bpy.context.scene

# 렌더링 설정
scene.render.engine = 'CYCLES'  # 예시로 CYCLES 렌더링 엔진을 사용
scene.render.resolution_x = 960
scene.render.resolution_y = 960
scene.render.fps = 24
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.filepath = output_path
scene.frame_start = start_frame
scene.frame_end = end_frame

# 렌더링 시작
print("🎬 렌더링 시작")
bpy.ops.render.render(animation=True)
print(f"✅ 렌더링 완료: {output_path}")
