import React from "react";
import {useNavigate} from "react-router-dom";
import NavBar from "../components/NavBar";

const FOLDER_COUNT = 3; // 영상 폴더 수, 필요시 수정

export default function SignAvatarListPage() {
    const navigate = useNavigate();

    // 폴더 기준으로 영상 데이터 생성 함수
    function generateVideoList() {
        const list = [];
        for (let i = 1; i <= FOLDER_COUNT; i++) {
            const folder = i.toString();
            list.push({
                id: folder,
                title: `영상 ${folder}`,
                thumbnail: `/videos/${folder}/thumb1.png`,
                videoUrl: `/videos/${folder}/main.mp4`,
                avatarData: [
                    {speaker: 1, videoUrl: `/videos/${folder}/avatar1.mp4`},
                    {speaker: 2, videoUrl: `/videos/${folder}/avatar2.mp4`},
                    {speaker: 3, videoUrl: `/videos/${folder}/avatar3.mp4`},
                    {speaker: 4, videoUrl: `/videos/${folder}/avatar4.mp4`},
                ],
                subtitleUrl: `/videos/${folder}/timestamp.json`,
            });
        }
        return list;
    }

    const videoList = generateVideoList();

    const onClickVideo = (video) => {
        // id로만 이동, 실제 데이터는 상세 페이지에서 로딩
        navigate(`/video?id=${video.id}`);
    };

    return (
        <>
            <NavBar/>
            <div style={{padding: 20}}>
                <h1>영상 목록</h1>
                <div style={{display: "flex", gap: 16, flexWrap: "wrap"}}>
                    {videoList.map((video) => (
                        <div
                            key={video.id}
                            style={{
                                width: 200,
                                cursor: "pointer",
                                textAlign: "center",
                                border: "1px solid #ddd",
                                borderRadius: 8,
                                padding: 10,
                            }}
                            onClick={() => onClickVideo(video)}
                        >
                            <img
                                src={video.thumbnail}
                                alt={video.title}
                                style={{width: "100%", height: 120, objectFit: "cover", borderRadius: 6}}
                            />
                            <div style={{marginTop: 8, fontWeight: "bold"}}>{video.title}</div>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}
