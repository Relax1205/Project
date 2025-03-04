import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import ThemeToggle from "./components/ThemeToggle";
import Home from "./pages/Home";
import About from "./pages/About";
import AuthModal from "./components/AuthModal";
import "./styles.css";

const AnimatedRoutes = () => {
    const location = useLocation();
    const [transitionClass, setTransitionClass] = useState("page-enter");

    useEffect(() => {
        setTransitionClass("page-enter-active");
        const timeout = setTimeout(() => {
            setTransitionClass("page-exit");
        }, 500);
        return () => clearTimeout(timeout);
    }, [location.pathname]);

    return (
        <div className={`page-transition ${transitionClass}`}>
            <Routes location={location} key={location.pathname}>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
            </Routes>
        </div>
    );
};

const App = () => {
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light-theme");
    const [isAuthModalOpen, setAuthModalOpen] = useState(false);

    useEffect(() => {
        document.body.className = theme;
        localStorage.setItem("theme", theme);
    }, [theme]);

    return (
        <Router>
            <div className="app-container">
                <Navbar onAuthClick={() => setAuthModalOpen(true)} />
                <ThemeToggle theme={theme} setTheme={setTheme} />
                <AnimatedRoutes />
                {isAuthModalOpen && <AuthModal onClose={() => setAuthModalOpen(false)} />}
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
