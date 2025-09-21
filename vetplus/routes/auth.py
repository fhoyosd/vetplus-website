from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required

from vetplus.models import User, ResetToken
from vetplus.utils import verify_recaptcha, generate_reset_token, send_reset_email
from vetplus.extensions import db, bcrypt

from datetime import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email")
        phone = request.form.get("phone")
        name = request.form.get("name")
        address = request.form.get("address")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        recaptcha_response = request.form.get("g-recaptcha-response")
        if not verify_recaptcha(recaptcha_response):
            return render_template("auth/register.html", captcha_error = "Captcha inválido, inténtalo de nuevo")

        user = User(username, hashed_password, name, "owner", email, phone, address)
        db.session.add(user)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión con tu cuenta.")

        return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html")

@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        recaptcha_response = request.form.get("g-recaptcha-response")
        if not verify_recaptcha(recaptcha_response):
            return render_template("auth/login.html", captcha_error = "Captcha inválido, inténtalo de nuevo")

        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for("main.home"))
        else:
            flash("Usuario o contraseña incorrectos")
        
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email = email).first()

        if not user:
            flash("No existe un usuario con ese correo.", "error")
            return redirect(url_for("auth.forgot_password"))

        # Generar token y enviar correo
        token = generate_reset_token(user.id)
        send_reset_email(user, token)
        flash("Se ha enviado un correo con instrucciones.", "success")
        return redirect(url_for("auth.forgot_password"))

    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    reset_token = ResetToken.query.filter_by(token = token).first()

    if not reset_token or reset_token.expires_at.replace(tzinfo = None) < datetime.now():
        flash("El enlace ha expirado o no es válido.", "error")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_password = request.form["password"]
        user = reset_token.user
        user.password = bcrypt.generate_password_hash(new_password)
        db.session.delete(reset_token)
        db.session.commit()

        flash("Tu contraseña ha sido cambiada exitosamente.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token = token)