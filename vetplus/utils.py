import requests
import secrets

from config import RECAPTCHA_SECRET_KEY
from .models import db, User, ResetToken
from .extensions import mail

from datetime import datetime, timedelta, timezone

from flask import abort
from flask_login import current_user
from flask_mail import Message

def verify_recaptcha(response_token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": response_token
    }
    r = requests.post(url, data = payload)
    print(r.json())
    
    return r.json().get("success", False)

def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)

def generate_reset_token(user_id):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(tz = timezone.utc) + timedelta(hours = 1)

    reset_token = ResetToken(user_id = user_id, token = token, expires_at = expires_at)
    db.session.add(reset_token)
    db.session.commit()

    return token



def send_reset_email(user, token):
    reset_link = f"http://127.0.0.1:5000/reset_password/{token}"
    msg = Message("Recupera tu contraseña - Vet Plus", recipients = [user.email])
    msg.body = f"""Hola {user.username},

Has solicitado recuperar tu contraseña. Haz clic en el siguiente enlace:

{reset_link}

Este link expira en 1 hora y solo se puede usar una vez.

Si no fuiste tú, ignora este correo.
"""
    mail.send(msg)