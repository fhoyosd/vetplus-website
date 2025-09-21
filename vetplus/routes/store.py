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

    return render_template("store/store.html", products = products, categories = categories, category_id = category_id, min_price = min_price, max_price = max_price)