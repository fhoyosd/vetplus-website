from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from vetplus.extensions import db, bcrypt
from vetplus.models import User
from vetplus.utils import admin_required

users_bp = Blueprint("users", __name__)

@users_bp.route("/users")
@login_required
def manage_users():
    admin_required()
    users = User.query.all()
    return render_template("admin/users/manage_users.html", users = users)

@users_bp.route("/users/create", methods = ["GET", "POST"])
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
            return redirect(url_for("users.manage_users"))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username, hashed_pw, name, role, email, phone, address)
        db.session.add(user)
        db.session.commit()

        flash("Usuario creado exitosamente", "success")
        return redirect(url_for("users.manage_users"))

    users = User.query.all()
    return render_template("admin/users/manage_users.html", users=users)

@users_bp.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
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
        return redirect(url_for("users.manage_users"))

    return render_template("admin/users/edit_user.html", user=user)

@users_bp.route("/users/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    admin_required()
    user = User.query.get_or_404(user_id)
    if user.role == "admin":
        flash("No se puede eliminar la cuenta administrador.", "danger")
        return redirect(url_for("users.manage_users"))

    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("users.manage_users"))
