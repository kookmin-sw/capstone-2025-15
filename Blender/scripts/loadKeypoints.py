import bpy
import json
from mathutils import Vector, Quaternion

json_path = bpy.path.abspath("//../keypoints/가다_pose3d.json")

body_map = {
    0: ("pelvis", 1),
    10: ("head", 11),
    11: ("upperarm_1.L", 13),
    12: ("upperarm_1.R", 14),
    13: ("forearm_1.L", 15),
    14: ("forearm_1.R", 16),
    15: ("palm.L", 13),
    16: ("palm.R", 14),
}

hand_finger_map_L = {
    (1, 2): "thumb_01.L",
    (5, 6): "index_01.L",
    (9,10): "middle_01.L",
    (13,14): "ring_01.L",
    (17,18): "pinky_01.L",
}
hand_finger_map_R = {
    (1, 2): "thumb_01.R",
    (5, 6): "index_01.R",
    (9,10): "middle_01.R",
    (13,14): "ring_01.R",
    (17,18): "pinky_01.R",
}

armature = bpy.data.objects["Armature"]
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

for pbone in armature.pose.bones:
    pbone.rotation_mode = 'QUATERNION'
    pbone.rotation_quaternion = (1, 0, 0, 0)
    pbone.location = (0, 0, 0)
    pbone.keyframe_delete(data_path="rotation_quaternion")
    pbone.keyframe_delete(data_path="location")

print("reset")

with open(json_path, "r", encoding="utf-8") as f:
    frames = json.load(f)

for frame_data in frames:
    frame = frame_data["frame"]
    body = frame_data["body_3d"]
    hand_L = frame_data.get("hand_left_3d", [])
    hand_R = frame_data.get("hand_right_3d", [])

    for i, (bone_name, j) in body_map.items():
        try:
            head = Vector((body[i][0], body[i][2], -body[i][1]))
            tail = Vector((body[j][0], body[j][2], -body[j][1]))
            direction = (tail - head).normalized()

            rest_bone = armature.data.bones[bone_name]

            if bone_name.startswith(("upperarm", "forearm")):
                local_axis = rest_bone.y_axis.normalized()
            elif bone_name.startswith("palm"):
                local_axis = rest_bone.x_axis.normalized()
            else:
                local_axis = (rest_bone.tail_local - rest_bone.head_local).normalized()

            rot = local_axis.rotation_difference(direction)
            
            fix = Quaternion((0, 0, 1), 0.0)
            if bone_name == "head":
                fix = (
                    Quaternion((0, 1, 0), 0.5) @
                    Quaternion((0, 0, 1), -0.5) @
                    Quaternion((1, 0, 0), -1.5)
                )
            elif "palm.L" == bone_name:
                fix = Quaternion((1, 0, 0), -0.6)
            elif "forearm_1.L" == bone_name:
                fix = (
                    Quaternion((0, 0, 1), -1.6) @
                    Quaternion((0, 1, 0), 2.5) @
                    Quaternion((1, 0, 0), 2.5)
                )
            elif "forearm_1.R" == bone_name:
                fix = (
                    Quaternion((0, 0, 1), -1.6) @
                    Quaternion((0, 1, 0), -2.5) @
                    Quaternion((1, 0, 0), -2.5)
                )
            elif "palm.R" == bone_name:
                fix = Quaternion((0, 0, 1), -0.2)
            rot = fix @ rot

            offset = Vector((0, 0, 0))
            if bone_name == "palm.L":
                offset = Vector((-0.03, 0.0, 0.02))
            elif bone_name == "palm.R":
                offset = Vector((0.03, 0.0, 0.02))
            elif bone_name == "forearm_1.L":
                offset = Vector((-0.01, 0.0, 0.03))
            elif bone_name == "forearm_1.R":
                offset = Vector((0.01, 0.0, 0.03))

            pbone = armature.pose.bones[bone_name]
            pbone.rotation_quaternion = rot
            pbone.keyframe_insert(data_path="rotation_quaternion", frame=frame + 1)

            if bone_name in ["pelvis", "head", "upperarm_1.R", "forearm_1.R", "palm.L", "palm.R"]:
                pbone.location = head + offset
                pbone.keyframe_insert(data_path="location", frame=frame + 1)

        except Exception as e:
            print(f"[!] {bone_name} fail: {e}")

    if hand_L:
        for (i, j), bone_name in hand_finger_map_L.items():
            try:
                head = Vector((hand_L[i][0], hand_L[i][2], -hand_L[i][1]))
                tail = Vector((hand_L[j][0], hand_L[j][2], -hand_L[j][1]))
                direction = (tail - head).normalized()

                rest_bone = armature.data.bones[bone_name]
                local_axis = rest_bone.x_axis.normalized()

                rot = local_axis.rotation_difference(direction)
                fix = Quaternion((0, 0, 1), 0.05)
                rot = fix @ rot

                pbone = armature.pose.bones[bone_name]
                pbone.rotation_quaternion = rot
                pbone.keyframe_insert(data_path="rotation_quaternion", frame=frame + 1)

            except Exception as e:
                print(f"[!] {bone_name} fail (left): {e}")
                
    if hand_R:
        for (i, j), bone_name in hand_finger_map_R.items():
            try:
                head = Vector((hand_R[i][0], hand_R[i][2], -hand_R[i][1]))
                tail = Vector((hand_R[j][0], hand_R[j][2], -hand_R[j][1]))
                direction = (tail - head).normalized()

                rest_bone = armature.data.bones[bone_name]
                local_axis = rest_bone.x_axis.normalized()

                rot = local_axis.rotation_difference(direction)
                fix = Quaternion((0, 0, 1), -0.05)
                rot = fix @ rot

                pbone = armature.pose.bones[bone_name]
                pbone.rotation_quaternion = rot
                pbone.keyframe_insert(data_path="rotation_quaternion", frame=frame + 1)

            except Exception as e:
                print(f"[!] {bone_name} fail (right): {e}")

    print(f"✅ Frame {frame} success")

print("done.")
