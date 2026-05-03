from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
import hashlib
import re

app = Flask(__name__)
app.secret_key = 'testsecretkey'
DATABASE = 'Users.db'

# --- Функции БД ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Логика валидации ---
def check_password_security(password):
    if len(password) < 8: return "Пароль должен быть не менее 8 символов."
    if not re.search(r"\d", password): return "Нужна хотя бы одна цифра."
    if not re.search(r"[A-Z]", password): return "Нужна хотя бы одна заглавная буква."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password): return "Нужен спецсимвол."
    return None

# --- Маршруты ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name, email, password = request.form['name'], request.form['email'], request.form['password']
    
    # Проверка пароля через нашу функцию
    error = check_password_security(password)
    if error:
        flash(error, "error")
        return redirect(url_for('index'))
    
    db = get_db()
    if db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
        flash("Email уже занят", "error")
        return redirect(url_for('index'))
    
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    db.execute("INSERT INTO users (name, password, email) VALUES (?, ?, ?)", (name, hashed_pw, email))
    db.commit()
    flash("Регистрация успешна!", "success")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        user = get_db().execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_pw)).fetchone()
        if user:
            session.update({'user_id': user['id'], 'user_name': user['name']})
            return redirect(url_for('profile'))
        flash("Неверный email или пароль", "error")
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', name=session.get('user_name')) if 'user_id' in session else redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        get_db().execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, email TEXT)')
    app.run(debug=True)
