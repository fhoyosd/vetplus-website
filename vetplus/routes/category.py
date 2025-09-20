from flask import Blueprint, render_template, request, redirect, url_for

from vetplus.extensions import db
from vetplus.models import Category

category_bp = Blueprint("category", __name__)

@category_bp.route("/categories", methods = ["GET"])
def manage_categories():
    categories = Category.query.all()
    return render_template("categories/manage_categories.html", categories = categories)

@category_bp.route("/categories/create_category", methods = ["POST"])
def create_category():
    name = request.form["name"]
    description = request.form.get("description")
    new_category = Category(name, description)

    db.session.add(new_category)
    db.session.commit()

    return redirect(url_for("category.manage_categories"))

@category_bp.route("/categories/edit/<int:category_id>", methods = ["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.name = request.form["name"]
        category.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("category.manage_categories"))
    return render_template("categories/edit_category.html", category = category)

@category_bp.route("/categories/delete/<int:category_id>", methods = ["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for("category.manage_categories"))
