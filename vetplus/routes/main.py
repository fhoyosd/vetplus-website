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

@main_bp.route("/informes")
def informes():
    return render_template("informes.html")

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

@main_bp.route("/consulta", methods=["GET", "POST"])
def consulta():
    if request.method == "POST":
        try:
            mascota = request.form.get("nombredemascota")
            dueno = request.form.get("nombrededueno")
            datos = request.form.get("datosdeconsulta")
            hora = request.form.get("hora")
            vet = request.form.get("veterinario")

            # 🔹 Validaciones backend
            if not mascota or not dueno or not datos or not hora or not vet:
                flash("⚠️ Todos los campos son obligatorios", "error")
                return redirect(url_for("main.consulta"))

            # Validar formato de hora (HH:MM)
            import re
            if not re.match(r'^\d{2}:\d{2}$', hora):
                flash("⚠️ La hora debe estar en formato HH:MM", "error")
                return redirect(url_for("main.consulta"))

            nueva = Consulta(
                nombredemascota = mascota,
                nombrededueno = dueno,
                datosdeconsulta = datos,
                hora = hora,
                veterinario = vet
            )
            db.session.add(nueva)
            db.session.commit()

            flash("Consulta guardada correctamente", "success")
            return redirect(url_for("main.consulta"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar la consulta: {str(e)}", "error")
            return redirect(url_for("main.consulta"))

    return render_template("dashboards/consultas/nueva_consulta.html")

@main_bp.route("/eliminar_consulta/<int:id>", methods = ["POST"])
def eliminar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()

    flash("Consulta eliminada con éxito!")
    
    return redirect(url_for("main.gestionar_consulta"))

@main_bp.route("/editar_consulta/<int:id>", methods = ["GET", "POST"])
def editar_consulta(id):
    consulta = Consulta.query.get_or_404(id)

    if request.method == "POST":
        consulta.nombredemascota = request.form["nombredemascota"]
        consulta.nombrededueno = request.form["nombrededueno"]
        consulta.datosdeconsulta = request.form["datosdeconsulta"]
        consulta.hora = request.form["hora"]
        consulta.veterinario = request.form["veterinario"]
        db.session.commit()

        flash("Consulta actualizada correctamente", "success")

        return redirect(url_for("main.gestionar_consulta"))

    return render_template("editar_consulta.html", consulta=consulta)

@main_bp.route("/consulta_dia")
def consulta_dia():
    try:
        consultas = Consulta.query.order_by(Consulta.id.desc()).limit(5).all()
    except Exception as e:
        print("⚠️ Error cargando consultas:", e)
        consultas = []

    return render_template("dashboards/consultas/consulta_dia.html", consulta_dia = consultas)

@main_bp.route("/registro_medico")
def registro_medico():
    return render_template("dashboards/consultas/registro_medico.html")

@main_bp.route("/gestionar_consulta")
def gestionar_consulta():
    consultas = Consulta.query.all()

    return render_template("gestionar_consulta.html", consultas = consultas)

@main_bp.route("/api/consultas")
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

@main_bp.route("/api/consultas/<int:id>", methods=["GET"])
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


# --- API: EDITAR CONSULTA ---
@main_bp.route("/api/consultas/<int:id>", methods=["PUT"])
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


# --- API: ELIMINAR CONSULTA ---
@main_bp.route("/api/consultas/<int:id>", methods=["DELETE"])
def api_consulta_eliminar(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({"message": "Consulta eliminada correctamente"})