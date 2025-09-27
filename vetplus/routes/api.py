from flask import Blueprint, jsonify, request

from vetplus.models import Order, OrderDetail, Consulta
from vetplus.extensions import db

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/invoice/<int:order_id>")
def invoice_json(order_id):
    order = Order.query.get_or_404(order_id)
    items = OrderDetail.query.filter_by(order_id=order.id).all()
    data = {
        "id": order.id,
        "full_name": order.full_name,
        "total": order.total,
        "status": order.status,
        "items": [
            {
                "product_name": i.product.name if i.product else "N/A",
                "quantity": i.quantity,
                "subtotal": i.subtotal
            }
            for i in items
        ]
    }
    return jsonify(data)

@api_bp.route("/api/consultas")
def api_consultas():
    consultas = Consulta.query.all()
    data = [
        {
            "id": c.id,
            "nombredemascota": c.nombredemascota,
            "nombrededueno": c.nombrededueno,
            "datosdeconsulta": c.datosdeconsulta,
            "hora": c.hora,
            "veterinario": c.veterinario
        }
        for c in consultas
    ]
    return jsonify(data)

@api_bp.route("/api/consultas/<int:id>", methods = ["GET"])
def api_consulta_detalle(id):
    consulta = Consulta.query.get_or_404(id)
    return jsonify({
        "id": consulta.id,
        "nombredemascota": consulta.nombredemascota,
        "nombrededueno": consulta.nombrededueno,
        "datosdeconsulta": consulta.datosdeconsulta,
        "hora": consulta.hora,
        "veterinario": consulta.veterinario
    })

@api_bp.route("/api/consultas/<int:id>", methods = ["PUT"])
def api_consulta_editar(id):
    consulta = Consulta.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "No se enviaron datos"}), 400

    consulta.nombredemascota = data.get("nombredemascota", consulta.nombredemascota)
    consulta.nombrededueno = data.get("nombrededueno", consulta.nombrededueno)
    consulta.datosdeconsulta = data.get("datosdeconsulta", consulta.datosdeconsulta)
    consulta.hora = data.get("hora", consulta.hora)
    consulta.veterinario = data.get("veterinario", consulta.veterinario)

    db.session.commit()
    return jsonify({"message": "Consulta actualizada correctamente"})

@api_bp.route("/api/consultas/<int:id>", methods = ["DELETE"])
def api_consulta_eliminar(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({"message": "Consulta eliminada correctamente"})