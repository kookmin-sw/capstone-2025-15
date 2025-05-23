
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

emotion_path = bpy.path.abspath("//../keypoints/emotion_result.json")
with open(emotion_path, "r", encoding="utf-8") as f:
    emotion_data = {d["frame"]: d["emotion"] for d in json.load(f)}

emotion_shape_map = {
    "기쁨": {
        "Smile_L": 0.8, "Smile_R": 0.8,
        "BrowUp_L": 0.5, "BrowUp_R": 0.5,
        "EyeWide_L": 0.2, "EyeWide_R": 0.2
    },
    "슬픔": {
        "MouthDown": 0.6, "BrowInnerUp": 0.5,
        "EyeBlink_L": 0.3, "EyeBlink_R": 0.3
    },
    "놀람": {
        "MouthUp": 0.7,
        "EyeWide_L": 0.7, "EyeWide_R": 0.7,
        "BrowUp_L": 0.6, "BrowUp_R": 0.6
    },
    "분노": {
        "BrowDown_L": 0.8, "BrowDown_R": 0.8,
        "JawClose": 0.6,
        "EyeSquint_L": 0.4, "EyeSquint_R": 0.4
    },
    "공포": {
        "MouthDown": 0.5,
        "EyeWide_L": 0.6, "EyeWide_R": 0.6,
        "BrowInner_L": 0.4, "BrowInner_R": 0.4
    },
    "중립": {}
}

def normalize(val, min_val=0.005, max_val=0.03):
    val = max(min(val, max_val), min_val)
    return (val - min_val) / (max_val - min_val)

prev_values = {}
SMOOTHING = 0.7

for frame_data in frames:
    frame = frame_data["frame"]
    face = frame_data.get("face_3d", [])
    if len(face) < max(BROW_R, MOUTH_BOTTOM):
        continue

    top = Vector(face[MOUTH_TOP])
    bottom = Vector(face[MOUTH_BOTTOM])
    mouth_open = (top - bottom).length

    left = Vector(face[MOUTH_LEFT])
    right = Vector(face[MOUTH_RIGHT])
    smile_dist = (left - right).length

    eye_L = (Vector(face[EYE_L_1]) - Vector(face[EYE_L_2])).length
    eye_R = (Vector(face[EYE_R_1]) - Vector(face[EYE_R_2])).length

    brow_avg = (face[BROW_L][1] + face[BROW_R][1]) / 2

    values = {
        "JawOpen": normalize(mouth_open, 0.005, 0.03),
        "Smile_L": normalize(smile_dist, 0.03, 0.06),
        "Smile_R": normalize(smile_dist, 0.03, 0.06),
        "EyeBlink_L": 1.0 - normalize(eye_L, 0.002, 0.015),
        "EyeBlink_R": 1.0 - normalize(eye_R, 0.002, 0.015),
        "BrowUp_L": normalize(brow_avg, 0.08, 0.12),
        "BrowUp_R": normalize(brow_avg, 0.08, 0.12),
    }

    emotion = emotion_data.get(frame, "중립")
    if isinstance(emotion, str):
        for k, v in emotion_shape_map.get(emotion, {}).items():
            values[k] = values.get(k, 0.0) + v

    for key, new_val in values.items():
        if key not in shape_keys:
            continue
        prev = prev_values.get(key, 0.0)
        smoothed = (1 - SMOOTHING) * prev + SMOOTHING * new_val
        shape_keys[key].value = smoothed
        shape_keys[key].keyframe_insert(data_path="value", frame=frame + 1)
        prev_values[key] = smoothed

