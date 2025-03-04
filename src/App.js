import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import ThemeToggle from "./components/ThemeToggle";
import Home from "./pages/Home";
import About from "./pages/About";
import AuthModal from "./components/AuthModal"; // Модальное окно входа/регистрации
import "./styles.css";

const App = () => {
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light-theme");
    const [isAuthModalOpen, setAuthModalOpen] = useState(false); // Состояние для модального окна

    useEffect(() => {
        document.body.className = theme;
        localStorage.setItem("theme", theme);
    }, [theme]);

    return (
        <Router>
            <div className="app-container">
                <Navbar onAuthClick={() => setAuthModalOpen(true)} /> {/* Передаем функцию открытия модалки */}
                <ThemeToggle theme={theme} setTheme={setTheme} />

                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<About />} />
                </Routes>

                {/* Модальное окно авторизации */}
                {isAuthModalOpen && <AuthModal onClose={() => setAuthModalOpen(false)} />}

                {/* Анимированные фигуры */}
                <div className="animated-bg">
                    <div className="shape"></div>
                    <div className="shape"></div>
                    <div className="shape"></div>
                </div>
            </div>
        </Router>
    );
};

export default App;
