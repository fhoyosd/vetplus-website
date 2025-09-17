from flask import Blueprint, render_template,  redirect, session, url_for
from flask_login import login_required, current_user

from vetplus.utils import admin_required
from vetplus.models import User

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if "username" in session:
        return redirect(url_for("menu"))
    return render_template("index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "owner":
        return render_template("dashboards/owner_dashboard.html", username = current_user, name = current_user.name)
    elif current_user.role == "admin":
        admin_required()
        users = User.query.all()
        return render_template("dashboards/admin_dashboard.html", username = current_user, name = current_user.name, users = users)
    else:
        return render_template("dashboards/vet_dashboard.html", username = current_user, name = current_user.name)