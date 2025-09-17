from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required

from vetplus.utils import admin_required
from vetplus.extensions import db, bcrypt
from vetplus.models import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    admin_required()
    user = User.query.get_or_404(user_id)
    if user.role == "admin":
        flash("No se puede eliminar la cuenta administrador.", "danger")
        return redirect(url_for("main.dashboard"))

    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("main.dashboard"))

@admin_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    admin_required()
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.name = request.form.get("name")
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        user.phone = request.form.get("phone")
        user.address = request.form.get("address")
        new_password = request.form.get("password")
        if new_password:
            user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        user.role = request.form.get("role")

        db.session.commit()
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("admin/edit_user.html", user=user)

@admin_bp.route("/create_user", methods=["GET", "POST"])
@login_required
def create_user():
    admin_required()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        role = request.form.get("role")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Ese usuario ya existe", "danger")
            return redirect(url_for("admin.create_user"))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        vet = User(username, hashed_pw, name, role, email, phone, address)
        db.session.add(vet)
        db.session.commit()

        flash("Usuario creado exitosamente", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("admin/create_user.html")