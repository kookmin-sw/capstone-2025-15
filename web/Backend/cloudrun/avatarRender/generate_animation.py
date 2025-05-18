import bpy
import json
from mathutils import Vector, Quaternion
import datetime

print("▶ 실행 시각:", datetime.datetime.now())

# ────────────────────────── 사용자 설정 ──────────────────────────
JSON_PATH      = bpy.path.abspath("//../keypoints/ge_pose3d.json")
FRAME_START    = 0          # 0 프레임 = 기준 자세(T-Pose)
SLERP_FACTOR   = 0.5        # 프레임 보간(0 = 매우 부드럽게, 1 = 즉시 반영)
ROOT_BONE_NAME = "pelvis"   # Armature 이동 대신 특정 루트 본만 이동
MOVE_ARMATURE  = False      # True → Armature 오브젝트 이동, False → ROOT_BONE 이동
# ----------------------------------------------------------------

# ─── (H36M 17-joints) 키포인트 ↔ Armature 본 매핑 ──────────────
body_map = {
      0 : ("pelvis",      7),   # 힙 → Spine-3
     10 : ("head",        9),   # Head → Neck
     14 : ("upperarm_1.L",15),  # L-Shoulder → L-Elbow
     15 : ("forearm_1.L", 16),  # L-Elbow    → L-Wrist
     16 : ("palm.L",      15),  # L-Wrist    → L-Elbow (손바닥 방향)
     11 : ("upperarm_1.R",12),  # R-Shoulder → R-Elbow
     12 : ("forearm_1.R", 13),  # R-Elbow    → R-Wrist
     13 : ("palm.R",      12),  # R-Wrist    → R-Elbow
}

# ─── 축 재정의(본별) ─────────────────────────────────────────────
axis_overrides = {
    "upperarm_1.L": "x",
    "forearm_1.L":  "x",
    "palm.L":       "y",
    "upperarm_1.R": "z",
    "forearm_1.R":  "x",
    "palm.R":       "x",
}

# ─── 0 프레임 기준 자세(T-Pose) ─────────────────────────────────
# Rest Pose가 이미 정면 T-Pose면 빈 딕셔너리 그대로 두세요.
CANONICAL_POSE = {
    "upperarm_1.L": Quaternion((1.2, 0.3827, 0, 0)),  # 약 +45° 회전 (X축 기준)
    "upperarm_1.R": Quaternion((1.2, 0, 0, -0.3827)), # 약 -45° 회전
}
# ----------------------------------------------------------------

# ─── Armature 초기화 ────────────────────────────────────────────
arm = bpy.data.objects["Armature"]
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

for pb in arm.pose.bones:
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.location = (0, 0, 0)

    pb.keyframe_delete(data_path="rotation_quaternion")
    pb.keyframe_delete(data_path="location")

if MOVE_ARMATURE:
    arm.location = (0, 0, 0)
    arm.keyframe_delete(data_path="location")

print("▶ Armature 초기화 완료")

# ─── 0 프레임 기준 자세 키프레임 삽입 ─────────────────────────
for pb in arm.pose.bones:
    q = CANONICAL_POSE.get(pb.name, Quaternion())
    pb.rotation_quaternion = q
    pb.keyframe_insert(data_path="rotation_quaternion", frame=FRAME_START)

if MOVE_ARMATURE:
    arm.keyframe_insert(data_path="location", frame=FRAME_START)
else:
    root_pb = arm.pose.bones[ROOT_BONE_NAME]
    root_pb.keyframe_insert(data_path="location", frame=FRAME_START)

print("▶ 0 프레임 기준 자세(T-Pose) 저장 완료")

# ─── 키포인트 데이터 로드 ─────────────────────────────────────
with open(JSON_PATH, encoding="utf-8") as f:
    frames = json.load(f)

auto_fix, last_rot = {}, {}

# ─── 프레임 루프 ───────────────────────────────────────────────
for fdata in frames:
    src_idx  = fdata["frame"]                   # 원본 키포인트 프레임 번호(0,1,2…)
    tgt_idx  = src_idx + FRAME_START + 1        # 실제 타임라인 1,2,3… 프레임
    body3d   = fdata["body_3d"]

    # ---------- 1. 루트 위치 이동 ----------
    pelvis_pos = Vector((body3d[0][0], body3d[0][2], body3d[0][1]))  # H36M 0번
    if MOVE_ARMATURE:
        arm.location = pelvis_pos
        arm.keyframe_insert(data_path="location", frame=tgt_idx)
    else:
        root_pb = arm.pose.bones[ROOT_BONE_NAME]
        root_pb.location = pelvis_pos
        root_pb.keyframe_insert(data_path="location", frame=tgt_idx)

    # ---------- 2. 본 회전 ----------
    for k_idx, (b_name, tail_idx) in body_map.items():
        try:
            head = Vector((body3d[k_idx][0],  body3d[k_idx][2],  body3d[k_idx][1]))
            tail = Vector((body3d[tail_idx][0], body3d[tail_idx][2], body3d[tail_idx][1]))
            direction = (tail - head).normalized()

            rest_bone = arm.data.bones[b_name]
            ax = axis_overrides.get(b_name, None)
            if   ax == "x": local_axis = rest_bone.x_axis.normalized()
            elif ax == "y": local_axis = rest_bone.y_axis.normalized()
            elif ax == "z": local_axis = rest_bone.z_axis.normalized()
            else:           local_axis = (rest_bone.tail_local - rest_bone.head_local).normalized()

            raw_rot = local_axis.rotation_difference(direction)

            if src_idx == 0:
                canonical_rot = CANONICAL_POSE.get(b_name, Quaternion())
                auto_fix[b_name] = (canonical_rot @ raw_rot).inverted()
                out_rot = Quaternion()

            else:
                out_rot = auto_fix[b_name] @ raw_rot
                if b_name in last_rot:
                    out_rot = Quaternion.slerp(last_rot[b_name], out_rot, SLERP_FACTOR)

            last_rot[b_name] = out_rot
            pb = arm.pose.bones[b_name]
            pb.rotation_quaternion = out_rot
            pb.keyframe_insert(data_path="rotation_quaternion", frame=tgt_idx)

        except Exception as e:
            print(f"[!] {b_name} 실패: {e}")

print("✅ 애니메이션 생성 완료")
