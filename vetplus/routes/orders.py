from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from vetplus.models import Order
from vetplus.extensions import db

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders/manage")
@login_required
def manage_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("orders/manage_orders.html", orders=orders)

@orders_bp.route("/orders/<int:order_id>/edit", methods = ["GET", "POST"])
@login_required
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == "POST":
        new_status = request.form.get("status")
        if new_status in ["pending", "paid", "cancelled"]:
            order.status = new_status
            db.session.commit()
            flash("Estado del pedido actualizado correctamente", "success")
            return redirect(url_for("orders.manage_orders"))
        else:
            flash("Estado inválido", "danger")

    return render_template("orders/edit_order.html", order = order)

@orders_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)

    try:
        db.session.delete(order)
        db.session.commit()
        flash(f"Pedido #{order.id} eliminado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al eliminar el pedido.", "danger")

    return redirect(url_for("orders.manage_orders"))
