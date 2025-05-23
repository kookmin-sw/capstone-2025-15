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

axis_overrides = {
    "upperarm_1.L": "x",
    "forearm_1.L":  "x",
    "palm.L":       "x",
    "upperarm_1.R": "z",
    "forearm_1.R":  "x",
    "palm.R":       "x",
}

#female setting. avatar number: 2, 4
CANONICAL_POSE = {
    "upperarm_1.L": Quaternion((1.2, 0.3827, 0, 0)),
    "upperarm_1.R": Quaternion((1.2, 0, 0, -0.3827))
}

#male setting. avatar number: 1, 3
#CANONICAL_POSE = {
#    "upperarm_1.L": Quaternion((1.2, 0.6, -0.4, 0)),
#    "upperarm_1.R": Quaternion((1.2, -0.4, 0, -0.6))
#}

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

with open(JSON_PATH, encoding="utf-8") as f:
    frames = json.load(f)

auto_fix, last_rot = {}, {}

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

    for k_idx, (b_name, tail_idx) in body_map.items():
        try:
            if b_name == "palm.L":
                head = Vector((body3d[k_idx][0], body3d[k_idx][2], body3d[k_idx][1]))
                tail = Vector((hand_l_data[0][0], hand_l_data[0][2], hand_l_data[0][1]))
            elif b_name == "palm.R":
                head = Vector((body3d[k_idx][0], body3d[k_idx][2], body3d[k_idx][1]))
                raw_direction = (tail - head)
                if raw_direction.length < 0.01:
                    print(f"pass: {b_name}")
                    continue
                    
                direction = raw_direction.normalized()
                rest_bone = arm.data.bones[b_name]
                
                local_axis = rest_bone.x_axis.normalized()
                raw_rot = local_axis.rotation_difference(direction)
                
                if src_idx == 0:
                    canonical_rot = Quaternion((1.0, 0, 0, 0))
                    auto_fix[b_name] = canonical_rot
                    out_rot = canonical_rot
                else:
                    out_rot = last_rot.get(b_name, Quaternion((1.0, 0, 0, 0)))
                
                last_rot[b_name] = out_rot
                pb = arm.pose.bones[b_name]
                pb.rotation_quaternion = out_rot
                pb.keyframe_insert(data_path="rotation_quaternion", frame=tgt_idx)
                
                continue
            
            else:
                head = Vector((body3d[k_idx][0], body3d[k_idx][2], body3d[k_idx][1]))
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
            print(f"[!] {b_name} fail: {e}")

print("--finish--")
