from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify
from flask_login import current_user
from vetplus.models import Product

cart_bp = Blueprint("cart", __name__)

def init_cart():
    if "cart" not in session:
        session["cart"] = {}

@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get("cart", {})

    pid = str(product_id)
    if pid in cart:
        cart[pid]["quantity"] += 1
    else:
        cart[pid] = {"name": product.name, "price": float(product.price), "quantity": 1}

    session["cart"] = cart
    session.modified = True

    total_items = sum(i["quantity"] for i in cart.values())
    return jsonify({"message": f"{product.name} añadido", "cart_count": total_items}), 200

@cart_bp.route("/cart")
def view_cart():
    init_cart()
    cart = session["cart"]

    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render_template("store/cart.html", cart = cart, total = total)

@cart_bp.route("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    init_cart()
    cart = session["cart"]

    if str(product_id) in cart:
        del cart[str(product_id)]
        session.modified = True
        flash("Producto eliminado del carrito", "info")

    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    flash("Carrito vaciado", "info")
    return redirect(url_for("cart.view_cart"))
