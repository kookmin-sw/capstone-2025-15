import React from 'react';
import '../styles/SubtitlePanel.css';

export default function SubtitlePanel({subtitles, onTimestampClick}) {
    return (
        <div className="subtitle-panel">
            {subtitles.map((sub, idx) => (
                <div key={idx} className="subtitle-item" onClick={() => onTimestampClick(sub.start)}>
                    <span className="timestamp">[{formatTime(sub.start)}]</span>
                    <span className="text">{sub.text}</span>
                </div>
            ))}
        </div>
    );
}

function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
}
