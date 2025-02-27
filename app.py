import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "static"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создаем базу данных внутри контекста приложения
with app.app_context():
    db.create_all()

# Загрузка модели классификации
MODEL_PATH = "garbage_classifier.h5"
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    CLASS_NAMES = ["Бумага", "Стекло", "Металл", "Пластик", "Органика", "Другой"]
else:
    model = None
    CLASS_NAMES = []

# Главная страница
@app.route("/")
def home():
    return render_template("index.html")

# Регистрация
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Аккаунт создан! Теперь войдите в систему.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Авторизация
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("profile"))
        else:
            flash("Неверные данные!", "danger")
    return render_template("login.html")

# Личный кабинет (защищенная страница)
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    result = None
    image_path = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = "upload.jpg"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            image_path = url_for("static", filename=filename)

            if model:
                # Обработка изображения
                img = image.load_img(filepath, target_size=(224, 224))
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                # Предсказание
                predictions = model.predict(img_array)
                class_idx = np.argmax(predictions)
                result = CLASS_NAMES[class_idx]
            else:
                result = "Ошибка: Модель не загружена."

    return render_template("profile.html", result=result, image=image_path)

# Выход
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
