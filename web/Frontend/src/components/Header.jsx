import React from 'react';
import '../styles/Header.css';

export default function Header() {
    return (
        <header className="header">
            <div className="logo">온담</div>
            <nav>
                <a href="#">COMPANY</a>
                <a href="#">SERVICES</a>
                <a href="#">CONTACT US</a>
            </nav>
        </header>
    );
}
