from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from vetplus.models import User
from vetplus.utils import verify_recaptcha
from vetplus.extensions import db, bcrypt

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
            return render_template("register.html", captcha_error = "Captcha inválido, inténtalo de nuevo")

        user = User(username, hashed_password, name, "owner", email, phone, address)
        db.session.add(user)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión con tu cuenta.")

        return redirect(url_for("auth.login"))
    
    return render_template("register.html")

@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        recaptcha_response = request.form.get("g-recaptcha-response")
        if not verify_recaptcha(recaptcha_response):
            return render_template("login.html", captcha_error = "Captcha inválido, inténtalo de nuevo")

        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for("main.dashboard"))
        else:
            flash("Usuario o contraseña incorrectos")
        
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))