from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from flask_mail import Message

from vetplus.extensions import mail, db
from vetplus.utils import admin_required
from vetplus.models import User, Consulta

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "owner":
        return render_template("dashboards/owner_dashboard.html",
                               username = current_user,
                               name = current_user.name)
    elif current_user.role == "admin":
        admin_required()
        users = User.query.all()
        return render_template("dashboards/admin_dashboard.html",
                               username = current_user,
                               name = current_user.name,
                               users = users)
    else:
        return render_template("dashboards/vet_dashboard.html",
                               username = current_user,
                               name = current_user.name)

@main_bp.route("/contacto", methods = ["GET", "POST"])
def contacto():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        msg = Message(
            subject = f"Nuevo mensaje de {name} via formulario de contacto",
            recipients = ['contactovetplus@gmail.com'],
            body = f"Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message}"
        )
        mail.send(msg)

        flash("Tu mensaje fue enviado con éxito.", "success")
        return redirect(url_for("main.contacto"))
    return render_template("contacto.html")