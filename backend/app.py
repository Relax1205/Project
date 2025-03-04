from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Создание Flask-приложения
app = Flask(__name__)

# Настройки для базы данных
app.config['SECRET_KEY'] = 'your_secret_key'  # Секретный ключ для сессий и cookies
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite база данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение отслеживания изменений в базе данных
db = SQLAlchemy(app)

# Инициализация менеджера входа пользователей
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Страница, на которую будет перенаправляться пользователь при попытке доступа без авторизации

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Функция загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route('/')
def home():
    if current_user.is_authenticated:
        return f"Добро пожаловать, {current_user.username}!"
    else:
        return "Добро пожаловать на главную страницу! Пожалуйста, войдите или зарегистрируйтесь."

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверка, есть ли уже такой пользователь
        user = User.query.filter_by(username=username).first()
        if user:
            return "Пользователь с таким именем уже существует!"
        
        # Хэширование пароля
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Создание нового пользователя
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return "Регистрация прошла успешно! Теперь вы можете войти."

    return '''
    <form method="POST">
        <input type="text" name="username" placeholder="Имя пользователя" required><br>
        <input type="password" name="password" placeholder="Пароль" required><br>
        <button type="submit">Зарегистрироваться</button>
    </form>
    <a href="/login">Уже есть аккаунт? Войдите</a>
    '''

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Поиск пользователя в базе данных
        user = User.query.filter_by(username=username).first()
        
        # Проверка пароля
        if user and check_password_hash(user.password, password):
            login_user(user)
            return f"Добро пожаловать, {user.username}!"
        else:
            return "Неверное имя пользователя или пароль."
    
    return '''
    <form method="POST">
        <input type="text" name="username" placeholder="Имя пользователя" required><br>
        <input type="password" name="password" placeholder="Пароль" required><br>
        <button type="submit">Войти</button>
    </form>
    <a href="/register">Нет аккаунта? Зарегистрируйтесь</a>
    '''

# Страница профиля (требуется авторизация)
@app.route('/profile')
@login_required
def profile():
    return f"Здравствуйте, {current_user.username}!"

# Страница выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "Вы успешно вышли из системы."

# Инициализация базы данных (если база данных не существует)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создание всех таблиц
    app.run(debug=True, host="0.0.0.0")  # Открытие на всех интерфейсах
