import re
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Category, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'shop_secret_key_2024'

db.init_app(app)

# --- Flask-Login setup ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Password validation (from Auth) ---
def check_password_security(password):
    if len(password) < 8:
        return 'Пароль должен быть не менее 8 символов.'
    if not re.search(r'\d', password):
        return 'Нужна хотя бы одна цифра.'
    if not re.search(r'[A-Z]', password):
        return 'Нужна хотя бы одна заглавная буква.'
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\"\\|,.<>/?]', password):
        return 'Нужен хотя бы один специальный символ.'
    return None

# --- Seed initial data ---
def seed_data():
    if Category.query.count() == 0:
        electronics = Category(name='Электроника')
        clothing    = Category(name='Одежда')
        food        = Category(name='Продукты питания')
        db.session.add_all([electronics, clothing, food])
        db.session.commit()

        db.session.add_all([
            Product(name='Смартфон',   price=25000, category=electronics),
            Product(name='Ноутбук',    price=55000, category=electronics),
            Product(name='Футболка',   price=800,   category=clothing),
            Product(name='Джинсы',     price=2500,  category=clothing),
            Product(name='Шоколад',    price=150,   category=food),
        ])
        db.session.commit()

# ============================================================
#  Routes
# ============================================================

@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('catalog.html', categories=categories)

# --- Category products ---
@app.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('category_products.html', category=category, products=products)

# --- Registration ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        error = check_password_security(password)
        if error:
            flash(error, 'error')
            return redirect(url_for('register'))
        if password != confirm:
            flash('Пароли не совпадают.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Этот email уже зарегистрирован.', 'error')
            return redirect(url_for('register'))

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Добро пожаловать, ' + user.name + '!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Неверный email или пароль.', 'error')
    return render_template('login.html')

# --- Logout ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('index'))

# --- Profile ---
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# ============================================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)
