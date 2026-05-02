from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Category, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Настройка системы авторизации
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    # Пример создания категорий и товаров, если они еще не созданы
    if Category.query.count() == 0:
        electronics = Category(name='Электроника')
        clothing = Category(name='Одежда')
        db.session.add(electronics)
        db.session.add(clothing)
        db.session.commit()
        
        product1 = Product(name='Телефон', price=500, category=electronics)
        product2 = Product(name='Рубашка', price=30, category=clothing)
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

# Главная страница - каталог товаров
@app.route('/')
def index():
    categories = Category.query.all()  # Получаем все категории
    return render_template('catalog.html', categories=categories)

# Регистрация пользователей
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Авторизация пользователей
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Успешная авторизация!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'danger')
    return render_template('login.html')

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    
# Маршрут для отображения продуктов внутри категории
@app.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('category_products.html', category=category, products=products)

# Маршрут для отображения подробной информации о товаре
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)
