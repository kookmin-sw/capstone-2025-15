using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class AvatarAnimatorFromJson : MonoBehaviour
{
    [System.Serializable]
    public class Joint { public float x, y, z, w; }
    [System.Serializable]
    public class Vec3 { public float x, y, z; }
    [System.Serializable]
    public class HandData { public string label; public List<Vec3> landmarks; }
    [System.Serializable]
    public class BlendShapeEntry { public string key; public float value; }

    [System.Serializable]
    public class PoseFrame
    {
        public List<Joint> pose;
        public List<HandData> hands;
        public List<Vec3> face;
        public List<BlendShapeEntry> blendshapes;
    }

    private Dictionary<string, string> blendshapeMap = new Dictionary<string, string>()
    {
        { "jawOpen", "JawOpen" },
        { "jawLeft", "JawLeft" },
        { "jawRight", "JawRight" },
        { "mouthSmileLeft", "Smile_L" },
        { "mouthSmileRight", "Smile_R" },
        { "mouthFrownLeft", "Sad_L" },
        { "mouthFrownRight", "Sad_R" },
        { "mouthPucker", "MouthLeft" },
        { "eyeBlinkLeft", "EyeBlink_L" },
        { "eyeBlinkRight", "EyeBlink_R" },
        { "eyeSquintLeft", "EyeSquint_L" },
        { "eyeSquintRight", "EyeSquint_R" },
        { "eyeWideLeft", "EyeWide_L" },
        { "eyeWideRight", "EyeWide_R" },
        { "browInnerUp", "BrowUp_L" },
        { "browDownLeft", "BrowDown_L" },
        { "browDownRight", "BrowDown_R" },
        { "browOuterUpLeft", "BrowOuter_L" },
        { "browOuterUpRight", "BrowOuter_R" }
    };

    [Header("Settings")]
    public string folderName = "dataSet_test";
    public float frameRate = 30f;

    [Header("Pose Bone Mapping (33 slots)")]
    public Transform[] avatarBones = new Transform[33];

    [Header("Hand Bone Mapping (21 slots each)")]
    public Transform[] avatarHandBonesLeft = new Transform[21];
    public Transform[] avatarHandBonesRight = new Transform[21];

    [Header("Face BlendShape")]
    public SkinnedMeshRenderer faceRenderer;

    private int currentFrame = 1;
    private string folderPath;

    void Start()
    {
        folderPath = Path.Combine(Application.streamingAssetsPath, folderName);

        if (avatarBones.Length != 33)
            Debug.LogWarning("아바타 본  배열은 33개여야 합니다.");
        if (avatarHandBonesLeft.Length != 21 || avatarHandBonesRight.Length != 21)
            Debug.LogWarning("손 뼈 배열은 각각 21개여야 합니다.");

        StartCoroutine(PlayFrames());
    }

    IEnumerator PlayFrames()
    {
        WaitForSeconds wait = new WaitForSeconds(1f / frameRate);

        while (true)
        {
            string filename = $"{currentFrame:D6}.json";
            string fullPath = Path.Combine(folderPath, filename);

            if (!File.Exists(fullPath))
            {
                Debug.Log($"모든 프레임 재생 완료: {currentFrame - 1} 프레임");
                yield break;
            }

            string json = File.ReadAllText(fullPath);
            PoseFrame data = JsonUtility.FromJson<PoseFrame>(json);
            ApplyPoseToAvatar(data);

            currentFrame++;
            yield return wait;
        }
    }

    void ApplyPoseToAvatar(PoseFrame data)
    {
        for (int i = 0; i < data.pose.Count && i < avatarBones.Length; i++)
        {
            if (avatarBones[i] == null) continue;
            var q = new Quaternion(data.pose[i].x, data.pose[i].y, data.pose[i].z, data.pose[i].w);
            avatarBones[i].localRotation = q;
        }

        if (data.hands != null)
        {
            foreach (var hand in data.hands)
            {
                var bones = hand.label == "Left" ? avatarHandBonesLeft : avatarHandBonesRight;
                if (bones.Length == 21) ApplyHandRotations(hand, bones);
            }
        }

        if (data.blendshapes != null && faceRenderer != null)
        {
            ApplyJsonBlendShapes(data.blendshapes, faceRenderer);
        }
    }

    void ApplyHandRotations(HandData hand, Transform[] boneArray)
    {
        float scale = 1f;

        for (int i = 0; i < hand.landmarks.Count; i++)
        {
            if (boneArray[i] == null) continue;

            Vector3 current = new Vector3(hand.landmarks[i].x, hand.landmarks[i].y, -hand.landmarks[i].z) * scale;
            Vector3 next = (i % 4 != 3 && i + 1 < hand.landmarks.Count)
                ? new Vector3(hand.landmarks[i + 1].x, hand.landmarks[i + 1].y, -hand.landmarks[i + 1].z) * scale
                : current;

            Vector3 dir = next - current;
            if (dir.magnitude > 0.0001f)
            {
                Quaternion lookRotation = Quaternion.LookRotation(dir);
                Quaternion offset = Quaternion.Euler(-90, 0, 0);
                boneArray[i].localRotation = lookRotation * offset;
            }
        }
    }

    void ApplyJsonBlendShapes(List<BlendShapeEntry> entries, SkinnedMeshRenderer renderer)
    {
        foreach (var entry in entries)
        {
            if (blendshapeMap.ContainsKey(entry.key))
            {
                string unityName = blendshapeMap[entry.key];
                int index = renderer.sharedMesh.GetBlendShapeIndex(unityName);
                if (index >= 0)
                {
                    float value = Mathf.Clamp01(entry.value) * 100f;
                    renderer.SetBlendShapeWeight(index, value);
                }
            }
        }
    }

    float Distance(Vec3 a, Vec3 b)
    {
        Vector3 va = new Vector3(a.x, a.y, -a.z);
        Vector3 vb = new Vector3(b.x, b.y, -b.z);
        return Vector3.Distance(va, vb);
    }
}
