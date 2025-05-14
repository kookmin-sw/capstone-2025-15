import React, {useEffect, useRef, useState} from 'react';
import Header from '../components/Header';
import VideoPlayer from '../components/VideoPlayer';
import SubtitlePanel from '../components/SubtitlePanel';
import '../styles/SignAvatarPage.css';

export default function SignAvatarPage({videoUrl, avatarData, subtitleData}) {
    const [currentTime, setCurrentTime] = useState(0);
    const [focusedSpeaker, setFocusedSpeaker] = useState(null);
    const [isMainPlaying, setIsMainPlaying] = useState(false);
    const videoRefs = useRef([]);

    const convertedSubtitles = subtitleData.map((s) => ({
        start: s.start / 1000,
        end: s.end / 1000,
        speaker: Number(s.speaker),
        text: s.sentence,
    }));

    const handleTimeUpdate = (time) => {
        setCurrentTime(time);
        const currentSubtitle = convertedSubtitles.find(
            (s) => time >= s.start && time <= s.end
        );
        if (currentSubtitle) {
            setFocusedSpeaker(Number(currentSubtitle.speaker));
        }
    };

    const handlePlayPause = (playing) => {
        setIsMainPlaying(playing);
    };

    const handleTimestampClick = (time) => {
        const video = document.getElementById('main-video');
        if (video) video.currentTime = time;
    };

    // ✅ 아바타 싱크 및 재생 제어 로직
    useEffect(() => {
        avatarData.forEach((avatar, index) => {
            const video = videoRefs.current[index];
            if (!video) return;

            const isFocused = Number(avatar.speaker) === Number(focusedSpeaker);

            // 싱크 맞추기
            if (Math.abs(video.currentTime - currentTime) > 0.5) {
                video.currentTime = currentTime;
            }

            // 재생/정지 제어
            if (isMainPlaying && isFocused) {
                if (video.paused) {
                    video.play().catch(() => {
                    });
                }
            } else {
                if (!video.paused) {
                    video.pause();
                }
            }
        });
    }, [avatarData, currentTime, focusedSpeaker, isMainPlaying]);

    return (<div className="container">
            <Header/>
            <div className="main-grid">
                <div className="grid-video">
                    <VideoPlayer
                        videoUrl={videoUrl}
                        onTimeUpdate={handleTimeUpdate}
                        onPlayPause={handlePlayPause}
                    />
                </div>

                <div className="grid-avatar">
                    {/* 메인 아바타 */}
                    {avatarData.map((avatar, index) =>
                        Number(avatar.speaker) === Number(focusedSpeaker) ? (
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
                        subtitles={convertedSubtitles}
                        onTimestampClick={handleTimestampClick}
                    />
                </div>

                <div className="grid-thumbnails">
                    {avatarData.map((avatar, index) =>
                        Number(avatar.speaker) !== Number(focusedSpeaker) ? (
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

    );
}
