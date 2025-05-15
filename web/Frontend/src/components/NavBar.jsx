import React from 'react';
import logo from '../assets/logo.png'; // 경로 조정 필요

export default function NavBar() {
    const styles = {
        navbar: {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative',
            backgroundColor: '#FFFF',
            padding: '0.5rem 1rem',
            color: 'black',
            height: '50px',
        },
        logoWrapper: {
            position: 'absolute',
            left: '1rem',
        },
        logo: {
            height: '100px',
        },
        menu: {
            listStyle: 'none',
            display: 'flex',
            margin: 0,
            padding: 0,
            gap: '1.5rem',
        },
        menuLink: {
            color: 'black',
            textDecoration: 'none',
            fontWeight: '700',       // 볼드체로 더 굵게
            fontSize: '1.2rem',      // 크기 키움
        },
    };


    return (
        <nav style={styles.navbar}>
            <ul style={styles.menu}>
                <li><a href="/list" style={styles.menuLink}>Home</a></li>
            </ul>
            <div style={styles.logoWrapper}>
                <img src={logo} alt="Logo" style={styles.logo}/>
            </div>
        </nav>
    );
}
