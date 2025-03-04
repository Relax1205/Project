import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api';

export const register = (username, password) => {
    return axios.post(`${API_URL}/register`, { username, password });
};

export const login = (username, password) => {
    return axios.post(`${API_URL}/login`, { username, password });
};

export const logout = () => {
    return axios.post(`${API_URL}/logout`);
};

export const classifyImage = (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_URL}/classify`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
};