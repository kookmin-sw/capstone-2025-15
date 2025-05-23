import React, {useEffect, useRef} from 'react';
import '../styles/VideoPlayer.css';

export default function VideoPlayer({videoUrl, onTimeUpdate, onPlayPause}) {
    const videoRef = useRef(null);

    useEffect(() => {
        const video = videoRef.current;
        if (!video) return;

        const handleTimeUpdate = () => onTimeUpdate(video.currentTime);
        const handlePlay = () => onPlayPause(true);
        const handlePause = () => onPlayPause(false);

        video.addEventListener('timeupdate', handleTimeUpdate);
        video.addEventListener('play', handlePlay);
        video.addEventListener('pause', handlePause);

        return () => {
            video.removeEventListener('timeupdate', handleTimeUpdate);
            video.removeEventListener('play', handlePlay);
            video.removeEventListener('pause', handlePause);
        };
    }, [onTimeUpdate, onPlayPause]);

    return (
        <div className="video-container">
            <video id="main-video" ref={videoRef} controls src={videoUrl}/>
        </div>
    );
}
