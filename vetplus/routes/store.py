from flask import Blueprint, render_template, redirect, session, url_for, request, flash
from flask_login import login_required, current_user

from vetplus.models import Product, Category

store_bp = Blueprint("store", __name__)

@store_bp.route("/tienda")
def tienda():
    category_id = request.args.get("category", type = int)
    min_price = request.args.get("min_price", type = float)
    max_price = request.args.get("max_price", type = float)

    query = Product.query

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price != None:
        query = query.filter(Product.price >= min_price)
    if max_price != None:
        query = query.filter(Product.price <= max_price)

    products = query.all()
    categories = Category.query.all()

    return render_template("store.html", products = products, categories = categories, category_id = category_id, min_price = min_price, max_price = max_price)

@store_bp.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash("Debes iniciar sesión para añadir productos al carrito.", "warning")
        return redirect(url_for("auth.login"))

    product = Product.query.get_or_404(product_id)
    if product.stock <= 0:
        flash("Este producto está agotado.", "danger")
        return redirect(url_for("store.tienda"))

    # Aquí va tu lógica de carrito (puedes guardarlo en sesión o tabla)
    cart = session.get("cart", [])
    cart.append(product_id)
    session["cart"] = cart
    flash(f"{product.name} añadido al carrito.", "success")
    return redirect(url_for("store.tienda"))