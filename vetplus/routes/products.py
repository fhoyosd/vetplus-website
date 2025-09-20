from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required

from vetplus.models import Product, Category
from vetplus.extensions import db
from vetplus.utils import admin_required

products_bp = Blueprint("products", __name__)

@products_bp.route("/products")
@login_required
def manage_products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template("products/manage_products.html", products = products, categories = categories)

@products_bp.route("/products/<int:product_id>")
@login_required
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return "No implementado aún"
    #return render_template("products/product_detail.html", product = product)

@products_bp.route("/products/create", methods = ["GET", "POST"])
@login_required
def create_product():
    admin_required()

    name = request.form["name"]
    description = request.form.get("description")
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    category_id = request.form.get("category_id")

    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id
    )
    db.session.add(new_product)
    db.session.commit()

    flash("Producto creado exitosamente.")

    return redirect(url_for("products.manage_products"))

@products_bp.route("/products/edit/<int:product_id>", methods = ["GET", "POST"])
@login_required
def edit_product(product_id):
    admin_required()

    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form.get("description")
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])
        product.category_id = request.form.get("category")
        db.session.commit()

        flash("Producto actualizado exitosamente.")
        
        return redirect(url_for("products.manage_products"))
    return render_template("products/edit_product.html", product=product, categories=categories)

@products_bp.route("/products/delete/<int:product_id>", methods = ["POST"])
@login_required
def delete_product(product_id):
    admin_required()

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("products.manage_products"))