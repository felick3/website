from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from src.models import get_db, init_db

app = Flask(__name__)
app.secret_key = "secret123"

@app.before_request
def setup():
    init_db()

@app.route("/")
def index():
    return render_template("index.html")

# -------- ПРОДУКТ --------
@app.route("/product/<int:id>")
def product_page(id):
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    return render_template("product.html", product=product)

# -------- API --------
@app.route("/api/products")
def products():
    db = get_db()
    rows = db.execute("SELECT * FROM products").fetchall()
    return jsonify([dict(r) for r in rows])

# -------- КОРЗИНА --------
@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    db = get_db()

    items = []
    total = 0

    for pid, qty in cart.items():
        p = db.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if p:
            item = dict(p)
            item["qty"] = qty
            item["sum"] = p["price"] * qty
            total += item["sum"]
            items.append(item)

    return render_template("cart.html", items=items, total=total)

@app.route("/add_to_cart/<int:id>", methods=["POST"])
def add_to_cart(id):
    cart = session.get("cart", {})

    cart[str(id)] = cart.get(str(id), 0) + 1
    session["cart"] = cart

    return jsonify({"status": "ok"})

@app.route("/remove_from_cart/<int:id>")
def remove_from_cart(id):
    cart = session.get("cart", {})
    cart.pop(str(id), None)
    session["cart"] = cart
    return redirect(url_for("cart"))

# -------- CHECKOUT --------
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        session["cart"] = {}
        return render_template("success.html")
    return render_template("checkout.html")

# -------- ПРОФИЛЬ --------
@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)