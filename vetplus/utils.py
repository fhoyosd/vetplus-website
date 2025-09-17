import requests

from config import RECAPTCHA_SECRET_KEY

from flask import abort
from flask_login import current_user

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