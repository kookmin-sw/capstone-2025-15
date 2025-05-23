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

json_path = bpy.path.abspath("//../keypoints/pose3d.json")

with open(json_path, "r", encoding="utf-8") as f:
    frames = json.load(f)

def normalize(val, min_val=0.005, max_val=0.03):
    val = max(min(val, max_val), min_val)
    return (val - min_val) / (max_val - min_val)

prev_values = {
    "JawOpen": 0.0,
    "Smile_L": 0.0,
    "Smile_R": 0.0,
    "EyeBlink_L": 0.0,
    "EyeBlink_R": 0.0,
    "BrowUp_L": 0.0,
    "BrowUp_R": 0.0,
    "Sad": 0.0,
    "Sad_L": 0.0,
    "Sad_R": 0.0,
    "BigSad": 0.0,
    "BigSad_L": 0.0,
    "BigSad_R": 0.0,
    "BrowAngry": 0.0,
    "BrowAngry_L": 0.0,
    "BrowAngry_R": 0.0,
}

SMOOTHING = 0.7

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

    angry_val = normalize(brow_avg, 0.10, 0.15)
    sad_val = normalize(brow_avg, 0.05, 0.09)

    values = {
        "JawOpen": normalize(mouth_open, 0.005, 0.03),
        "Smile_L": normalize(smile_dist, 0.03, 0.06),
        "Smile_R": normalize(smile_dist, 0.03, 0.06),
        "EyeBlink_L": 1.0 - normalize(eye_L, 0.002, 0.015),
        "EyeBlink_R": 1.0 - normalize(eye_R, 0.002, 0.015),
        "BrowUp_L": normalize(brow_avg, 0.08, 0.12),
        "BrowUp_R": normalize(brow_avg, 0.08, 0.12),
        "Sad": sad_val,
        "Sad_L": sad_val,
        "Sad_R": sad_val,
        "BigSad": sad_val,
        "BigSad_L": sad_val,
        "BigSad_R": sad_val,
        "BrowAngry": angry_val,
        "BrowAngry_L": angry_val,
        "BrowAngry_R": angry_val,
    }

    for key, new_val in values.items():
        if frame == 0:
            smoothed = new_val
        else:
            prev = prev_values[key]
            smoothed = (1 - SMOOTHING) * prev + SMOOTHING * new_val

        shape_keys[key].value = smoothed
        shape_keys[key].keyframe_insert(data_path="value", frame=frame + 1)
        prev_values[key] = smoothed
        
print("-- finish --")
