// src/components/Navbar.js
import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";
import AuthModal from "./AuthModal";  // Дефолтный импорт

const Navbar = ({ onAuthClick }) => {
    return (
        <nav className="navbar">
            <span className="navbar-title">Классификация мусора</span>
            <Link to="/">Главная</Link>
            <Link to="/about">О проекте</Link>
            <button className="auth-btn" onClick={onAuthClick}>Вход / Регистрация</button>
        </nav>
    );
};

export default Navbar;
