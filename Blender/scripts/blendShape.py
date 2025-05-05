import bpy
import json
from mathutils import Vector

MOUTH_TOP = 13
MOUTH_BOTTOM = 14
MOUTH_LEFT = 61
MOUTH_RIGHT = 291
EYE_L_1, EYE_L_2 = 159, 145
EYE_R_1, EYE_R_2 = 386, 374
BROW_L = 70
BROW_R = 300

head_obj = bpy.data.objects["head_mesh"]
shape_keys = head_obj.data.shape_keys.key_blocks

json_path = bpy.path.abspath("//../keypoints/가다_pose3d.json")

with open(json_path, "r", encoding="utf-8") as f:
    frames = json.load(f)

def normalize(val, min_val=0.005, max_val=0.03):
    val = max(min(val, max_val), min_val)
    return (val - min_val) / (max_val - min_val)

for frame_data in frames:
    frame = frame_data["frame"]
    face = frame_data.get("face_3d", [])

    if len(face) < max(MOUTH_BOTTOM, MOUTH_RIGHT, EYE_R_1, BROW_R):
        continue

    top = Vector(face[MOUTH_TOP])
    bottom = Vector(face[MOUTH_BOTTOM])
    mouth_open = (top - bottom).length

    left = Vector(face[MOUTH_LEFT])
    right = Vector(face[MOUTH_RIGHT])
    smile_dist = (left - right).length

    eye_L = (Vector(face[EYE_L_1]) - Vector(face[EYE_L_2])).length
    eye_R = (Vector(face[EYE_R_1]) - Vector(face[EYE_R_2])).length

    brow_L_y = face[BROW_L][1]
    brow_R_y = face[BROW_R][1]
    brow_avg = (brow_L_y + brow_R_y) / 2

    jaw_open_val = normalize(mouth_open, 0.005, 0.03)
    smile_val = normalize(smile_dist, 0.03, 0.06)
    blink_L_val = normalize(eye_L, 0.002, 0.015)
    blink_R_val = normalize(eye_R, 0.002, 0.015)
    brow_up_val = normalize(brow_avg, 0.08, 0.12)

    shape_keys["JawOpen"].value = jaw_open_val
    shape_keys["Smile_L"].value = smile_val
    shape_keys["Smile_R"].value = smile_val
    shape_keys["EyeBlink_L"].value = 1.0 - blink_L_val
    shape_keys["EyeBlink_R"].value = 1.0 - blink_R_val
    shape_keys["BrowUp_L"].value = brow_up_val
    shape_keys["BrowUp_R"].value = brow_up_val

    for key in ["JawOpen", "Smile_L", "Smile_R", "EyeBlink_L", "EyeBlink_R", "BrowUp_L", "BrowUp_R"]:
        shape_keys[key].keyframe_insert(data_path="value", frame=frame + 1)

print("success")
