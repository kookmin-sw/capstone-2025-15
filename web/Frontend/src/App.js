import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import SignAvatarPage from './pages/SignAvatarPage';
import avatarData from './data/avatarData';
import subtitleData from './data/subtitleData';

const videoUrl = "/videos/main.mp4"; // public 폴더 기준

function App() {
    return (
        <Router>
            <Routes>
                <Route
                    path="/video"
                    element={
                        <SignAvatarPage
                            videoUrl={videoUrl}
                            avatarData={avatarData}
                            subtitleData={subtitleData}
                        />
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
