import React from "react";
import "./ThemeToggle.css";

const ThemeToggle = ({ theme, setTheme }) => {
    const toggleTheme = () => {
        setTheme(theme === "light-theme" ? "dark-theme" : "light-theme");
    };

    return (
        <button className="theme-toggle" onClick={toggleTheme}>
            {theme === "light-theme" ? "🌙 Тёмная" : "☀️ Светлая"}
        </button>
    );
};

export default ThemeToggle;
