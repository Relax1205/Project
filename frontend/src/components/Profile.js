import React, { useState } from "react";
import { classifyImage } from "../services/api";
import "./Profile.css";

const Profile = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [result, setResult] = useState(null);
    const [imageURL, setImageURL] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError("Выберите файл перед загрузкой");
            return;
        }
        setError(null);
        try {
            const response = await classifyImage(selectedFile);
            setResult(response.data.result);
            setImageURL(response.data.image_url);
        } catch (err) {
            setError("Ошибка загрузки файла");
        }
    };

    return (
        <div className="profile-container">
            <h2>Классификация мусора</h2>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Определить</button>
            {error && <p className="error">{error}</p>}
            {result && (
                <div className="result-container">
                    <h3>Результат: {result}</h3>
                    {imageURL && <img src={imageURL} alt="Загруженное изображение" />}
                </div>
            )}
        </div>
    );
};

export default Profile;