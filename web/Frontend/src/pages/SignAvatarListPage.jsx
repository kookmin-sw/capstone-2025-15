import React from "react";
import {useNavigate} from "react-router-dom";
import NavBar from "../components/NavBar";
import '../styles/SignAvatarListPage.css'; // CSS 임포트 추가

const FOLDER_COUNT = 2; // 영상 폴더 수, 필요시 수정

export default function SignAvatarListPage() {
    const navigate = useNavigate();

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
        navigate(`/video?id=${video.id}`);
    };

    return (
        <>
            <NavBar/>
            <div className="page-container">
                <h1>영상 목록</h1>
                <div className="video-list">
                    {videoList.map((video) => (
                        <div
                            key={video.id}
                            className="video-card"
                            onClick={() => onClickVideo(video)}
                        >
                            <img
                                src={video.thumbnail}
                                alt={video.title}
                                className="video-thumbnail"
                            />
                            <div className="video-card-title">{video.title}</div>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}
