import React, {useEffect, useRef, useState} from "react";
import {useLocation, useNavigate} from "react-router-dom";
import VideoPlayer from "../components/VideoPlayer";
import SubtitlePanel from "../components/SubtitlePanel";
import "../styles/SignAvatarPage.css";
import NavBar from "../components/NavBar";

export default function SignAvatarPage() {
    const location = useLocation();
    const navigate = useNavigate();

    const [videoUrl, setVideoUrl] = useState(null);
    const [avatarData, setAvatarData] = useState([]);
    const [subtitleData, setSubtitleData] = useState([]);

    const [currentTime, setCurrentTime] = useState(0);
    const [focusedSpeaker, setFocusedSpeaker] = useState(1);
    const [isMainPlaying, setIsMainPlaying] = useState(false);
    const videoRefs = useRef([]);

    const params = new URLSearchParams(location.search);
    const folderId = params.get("id");

    useEffect(() => {
        if (!folderId) {
            alert("잘못된 접근입니다.");
            navigate("/");
            return;
        }

        // ✅ GCS 버킷의 public URL 사용
        const basePath = `https://storage.googleapis.com/capstone25-15-fe/demonstrationData/videos/${folderId}`;

        setVideoUrl(`${basePath}/main.mp4`);

        const avatars = [1, 2, 3, 4].map((n) => ({
            speaker: n,
            videoUrl: `${basePath}/avatar${n}.mp4`,
        }));
        setAvatarData(avatars);

        fetch(`${basePath}/timestamp.json`)
            .then((res) => res.json())
            .then((data) => setSubtitleData(data))
            .catch(() => {
                alert("자막 파일 로드 실패");
                setSubtitleData([]);
            });
    }, [folderId, navigate]);

    useEffect(() => {
        if (subtitleData.length === 0) {
            setFocusedSpeaker(1);
            return;
        }

        const currentSubtitle = subtitleData.find(
            (s) =>
                currentTime >= s.start / 1000 &&
                currentTime <= s.end / 1000
        );

        if (currentSubtitle) {
            setFocusedSpeaker(Number(currentSubtitle.speaker));
        }
    }, [currentTime, subtitleData]);

    useEffect(() => {
        avatarData.forEach((avatar, index) => {
            const video = videoRefs.current[index];
            if (!video) return;

            const isFocused = avatar.speaker === focusedSpeaker;

            if (Math.abs(video.currentTime - currentTime) > 0.5) {
                video.currentTime = currentTime;
            }

            if (isMainPlaying && isFocused) {
                if (video.paused) video.play().catch(() => {
                });
            } else {
                if (!video.paused) video.pause();
            }
        });
    }, [avatarData, currentTime, focusedSpeaker, isMainPlaying]);

    return (
        <>
            {!videoUrl ? (
                <div>로딩 중...</div>
            ) : (
                <div className="container">
                    <NavBar/>
                    <div className="main-grid">
                        <div className="grid-video">
                            <VideoPlayer
                                videoUrl={videoUrl}
                                onTimeUpdate={setCurrentTime}
                                onPlayPause={setIsMainPlaying}
                                id="main-video"
                            />
                        </div>

                        <div className="grid-avatar">
                            {avatarData.map((avatar, index) =>
                                avatar.speaker === focusedSpeaker ? (
                                    <video
                                        key={avatar.speaker}
                                        src={avatar.videoUrl}
                                        ref={(el) => (videoRefs.current[index] = el)}
                                        muted
                                        playsInline
                                        className="focused-avatar"
                                    />
                                ) : null
                            )}
                        </div>

                        <div className="grid-subtitle">
                            <SubtitlePanel
                                subtitles={subtitleData.map((s) => ({
                                    start: s.start / 1000,
                                    end: s.end / 1000,
                                    speaker: Number(s.speaker),
                                    text: s.sentence,
                                }))}
                                onTimestampClick={(time) => {
                                    const video = document.getElementById("main-video");
                                    if (video) video.currentTime = time;
                                }}
                            />
                        </div>

                        <div className="grid-thumbnails">
                            {avatarData.map((avatar, index) =>
                                avatar.speaker !== focusedSpeaker ? (
                                    <video
                                        key={avatar.speaker}
                                        src={avatar.videoUrl}
                                        ref={(el) => (videoRefs.current[index] = el)}
                                        muted
                                        playsInline
                                        className="thumbnail-avatar"
                                    />
                                ) : null
                            )}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}