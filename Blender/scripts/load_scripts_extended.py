import bpy
import json
from mathutils import Vector, Quaternion
import datetime

print("--Runtime:", datetime.datetime.now())

# ----------------------------------------------------------------
JSON_PATH      = bpy.path.abspath("//../keypoints/pose3d.json")
FRAME_START    = 0 
SLERP_FACTOR   = 0.5 
ROOT_BONE_NAME = "pelvis" 
MOVE_ARMATURE  = False 
# ----------------------------------------------------------------

body_map = {
      0 : ("pelvis",      7), 
     10 : ("head",        9),
     14 : ("upperarm_1.L",15),
     15 : ("forearm_1.L", 16), 
     16 : ("palm.L",      1),
     11 : ("upperarm_1.R",12),
     12 : ("forearm_1.R", 13),
     13 : ("palm.R",      1),
}

left_hand_map = {
    0: "palm.L",
    1: "thumb_01.L",
    2: "thumb_02.L",
    3: "thumb_03.L",
    #4: "thumb_04.L",
    5: "index_01.L",
    6: "index_02.L",
    7: "index_03.L",
    #8: "index_04.L",
    9: "middle_01.L",
    10:"middle_02.L",
    11:"middle_03.L",
    #12:"middle_04.L",
    13:"ring_01.L",
    14:"ring_02.L",
    15:"ring_03.L",
    #16:"ring_04.L",
    17:"pinky_01.L",
    18:"pinky_02.L",
    19:"pinky_03.L",
    #20:"pinky_04.L",
}

right_hand_map = {
    0: "wrist.R",
    1: "thumb_01.R",
    2: "thumb_02.R",
    3: "thumb_03.R",
    4: "thumb_04.R",
    5: "index_01.R",
    6: "index_02.R",
    7: "index_03.R",
    8: "index_04.R",
    9: "middle_01.R",
    10:"middle_02.R",
    11:"middle_03.R",
    12:"middle_04.R",
    13:"ring_01.R",
    14:"ring_02.R",
    15:"ring_03.R",
    16:"ring_04.R",
    17:"pinky_01.R",
    18:"pinky_02.R",
    19:"pinky_03.R",
    20:"pinky_04.R",
}

axis_overrides = {
    "upperarm_1.L": "x",
    "forearm_1.L":  "x",
    "palm.L":       "x",
    "upperarm_1.R": "z",
    "forearm_1.R":  "x",
    "palm.R":       "x",
}

CANONICAL_POSE = {
    "upperarm_1.L": Quaternion((1.2, 0.3827, 0, 0)),
    "upperarm_1.R": Quaternion((1.2, 0, 0, -0.3827))
}

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

print("-- Armature Reset --")

for pb in arm.pose.bones:
    q = CANONICAL_POSE.get(pb.name, Quaternion())
    pb.rotation_quaternion = q
    pb.keyframe_insert(data_path="rotation_quaternion", frame=FRAME_START)

if MOVE_ARMATURE:
    arm.keyframe_insert(data_path="location", frame=FRAME_START)
else:
    root_pb = arm.pose.bones[ROOT_BONE_NAME]
    root_pb.keyframe_insert(data_path="location", frame=FRAME_START)

auto_fix, last_rot = {}, {}

def get_local_axis(rest_bone, axis_key):
    if axis_key == "x":
        return rest_bone.x_axis.normalized()
    elif axis_key == "y":
        return rest_bone.y_axis.normalized()
    elif axis_key == "z":
        return rest_bone.z_axis.normalized()
    else:
        return (rest_bone.tail_local - rest_bone.head_local).normalized()

def apply_rotation(bone_name, head_pos, tail_pos, axis_key, frame_idx):
    rest_bone = arm.data.bones[bone_name]
    local_axis = get_local_axis(rest_bone, axis_key)
    direction = (tail_pos - head_pos).normalized()
    raw_rot = local_axis.rotation_difference(direction)
    if frame_idx == 0:
        canonical_rot = CANONICAL_POSE.get(bone_name, Quaternion())
        auto_fix[bone_name] = (canonical_rot @ raw_rot).inverted()
        out_rot = Quaternion()
    else:
        out_rot = auto_fix[bone_name] @ raw_rot
        if bone_name in last_rot:
            out_rot = Quaternion.slerp(last_rot[bone_name], out_rot, SLERP_FACTOR)
    last_rot[bone_name] = out_rot
    pb = arm.pose.bones[bone_name]
    pb.rotation_quaternion = out_rot
    pb.keyframe_insert(data_path="rotation_quaternion", frame=frame_idx)

with open(JSON_PATH, encoding="utf-8") as f:
    frames = json.load(f)

for fdata in frames:
    src_idx  = fdata["frame"]
    tgt_idx  = src_idx + FRAME_START + 1
    body3d   = fdata["body_3d"]
    hand_l_data = fdata.get("left_hand_3d", [])
    hand_r_data = fdata.get("right_hand_3d", [])

    pelvis_pos = Vector((body3d[0][0], body3d[0][2], body3d[0][1]))
    if MOVE_ARMATURE:
        arm.location = pelvis_pos
        arm.keyframe_insert(data_path="location", frame=tgt_idx)
    else:
        root_pb = arm.pose.bones[ROOT_BONE_NAME]
        root_pb.location = pelvis_pos
        root_pb.keyframe_insert(data_path="location", frame=tgt_idx)

    # 몸통 및 팔 처리
    for k_idx, (b_name, tail_idx) in body_map.items():
        if tail_idx is None:
            continue
        if b_name == "palm.L":
            head = Vector((body3d[k_idx][0], body3d[k_idx][2], body3d[k_idx][1]))
            tail = Vector((hand_l_data[0][0], hand_l_data[0][2], hand_l_data[0][1]))
            axis_key = axis_overrides.get(b_name, "x")
            apply_rotation(b_name, head, tail, axis_key, tgt_idx)
        elif b_name == "palm.R":
            head = Vector((body3d[k_idx][0], body3d[k_idx][2], body3d[k_idx][1]))
            tail = Vector((hand_r_data[0][0], hand_r_data[0][2], hand_r_data[0][1]))
            axis_key = axis_overrides.get(b_name, "x")
            apply_rotation(b_name, head, tail, axis_key, tgt_idx)
        else:
            head = Vector((body3d[k_idx][0], body3d[k_idx][2], body3d[k_idx][1]))
            tail = Vector((body3d[tail_idx][0], body3d[tail_idx][2], body3d[tail_idx][1]))
            axis_key = axis_overrides.get(b_name, None)
            apply_rotation(b_name, head, tail, axis_key, tgt_idx)

print("--finish--")
