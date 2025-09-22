import re

from flask import Blueprint, session, flash, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from flask_mail import Message

from vetplus.models import Product, Order, OrderDetail
from vetplus.extensions import db, mail

checkout_bp = Blueprint("checkout", __name__)

@checkout_bp.route("/checkout", methods = ["GET", "POST"])
@login_required
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("Tu carrito está vacío", "error")
        return redirect(url_for("cart.view_cart"))

    products = Product.query.filter(Product.id.in_(cart.keys())).all()
    total = sum(p.price * cart[str(p.id)]["quantity"] for p in products)

    if request.method == "POST":
        full_name = request.form["full_name"]
        address = request.form["address"]
        phone = request.form["phone"]
        payment_method = request.form["payment_method"]

        card_number = request.form.get("card_number")
        card_expiry = request.form.get("card_expiry")
        card_cvv = request.form.get("card_cvv")

        # Validaciones si es tarjeta
        if payment_method in ["Tarjeta de crédito", "Tarjeta de débito"]:
            if not re.fullmatch(r"\d{16,19}", card_number or ""):
                flash("Número de tarjeta inválido (mínimo 16 dígitos).", "danger")
                return redirect(url_for("checkout.checkout"))

            if not re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", card_expiry or ""):
                flash("Fecha de vencimiento inválida. Usa formato MM/YY.", "danger")
                return redirect(url_for("checkout.checkout"))

            if not re.fullmatch(r"\d{3,4}", card_cvv or ""):
                flash("CVV inválido (3 o 4 dígitos).", "danger")
                return redirect(url_for("checkout.checkout"))

        order = Order(
            user_id = current_user.id,
            full_name = full_name,
            address = address,
            phone = phone,
            payment_method = payment_method,
            total = total,
            status = "paid",
            card_number = card_number[-4:] if card_number else None,
            card_expiry = card_expiry if card_expiry else None,
        )
        db.session.add(order)
        db.session.flush()

        for p in products:
            qty = cart[str(p.id)]["quantity"]
            if p.stock < qty:
                flash(f"No hay suficiente stock de {p.name}", "error")
                return redirect(url_for("cart.view_cart"))
            p.stock -= qty
            detail = OrderDetail(
                order_id = order.id,
                product_id = p.id,
                quantity = qty,
                subtotal = p.price * qty
            )
            db.session.add(detail)

        db.session.commit()
        session.pop("cart", None)

        # Correo
        msg = Message(
            subject = "Confirmación de Pedido - VetPlus",
            recipients = [current_user.email],
            body = f"Gracias por tu compra. Tu pedido con ID #{order.id} fue confirmado."
        )
        mail.send(msg)

        return redirect(url_for("checkout.success", order_id = order.id))

    return render_template("checkout/checkout.html", products = products, cart = cart, total = total)

@checkout_bp.route("/success/<int:order_id>")
@login_required
def success(order_id):
    return render_template("checkout/success.html", order_id = order_id)

@checkout_bp.route("/invoice/<int:order_id>")
def invoice(order_id):
    order = Order.query.get_or_404(order_id)
    items = Product.query.filter_by(id = order_id).all()

    return render_template("checkout/invoice.html", order = order, items = items, user = current_user)
