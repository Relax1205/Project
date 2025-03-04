// src/components/AuthModal.js
import React, { useState } from "react";
import "./AuthModal.css";

const AuthModal = ({ onClose }) => {
    const [isLogin, setIsLogin] = useState(true);

    return (
        <div className="auth-modal">
            <div className="auth-content">
                <h2>{isLogin ? "Вход" : "Регистрация"}</h2>
                <form>
                    <input type="text" placeholder="Логин" required />
                    <input type="password" placeholder="Пароль" required />
                    {!isLogin && <input type="password" placeholder="Повторите пароль" required />}
                    <button type="submit">{isLogin ? "Войти" : "Зарегистрироваться"}</button>
                </form>
                <p onClick={() => setIsLogin(!isLogin)}>
                    {isLogin ? "Нет аккаунта? Зарегистрируйтесь" : "Уже есть аккаунт? Войти"}
                </p>
                <button className="close-btn" onClick={onClose}>Закрыть</button>
            </div>
        </div>
    );
};

export default AuthModal;  // Это дефолтный экспорт
