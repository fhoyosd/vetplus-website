from flask import Blueprint, render_template
from flask_login import login_required
from vetplus.utils import admin_required

admin_bp = Blueprint("admin", __name__)

# --- DASHBOARD ---
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    admin_required()
    return render_template("admin/admin_dashboard.html")

