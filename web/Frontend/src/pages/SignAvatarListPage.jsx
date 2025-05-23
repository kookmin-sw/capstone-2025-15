import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import NavBar from "../components/NavBar";

const FOLDER_COUNT = 2; // 영상 폴더 수, 필요시 수정

export default function SignAvatarListPage() {
    const navigate = useNavigate();

    // useEffect로 서버에서 받아오기
    const [videoList, setVideoList] = useState([]);

    useEffect(() => {
        fetch('/api/videos')
            .then((res) => res.json())
            .then(setVideoList)
            .catch(() => alert('영상 목록을 불러오지 못했습니다.'));
    }, []);


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
