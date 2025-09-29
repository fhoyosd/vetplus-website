from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask import jsonify

from vetplus.models import Consulta, RegistroMedico
from vetplus.extensions import db

consulta_bp = Blueprint("consulta", __name__)

@consulta_bp.route("/consulta", methods=["GET", "POST"])
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
                flash("Todos los campos son obligatorios", "error")
                return redirect(url_for("consulta.consulta"))

            # Validar formato de hora (HH:MM)
            import re
            if not re.match(r'^\d{2}:\d{2}$', hora):
                flash("La hora debe estar en formato HH:MM", "error")
                return redirect(url_for("consulta.consulta"))

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
            return redirect(url_for("consulta.consulta"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar la consulta: {str(e)}", "error")
            return redirect(url_for("consulta.consulta"))

    return render_template("dashboards/consultas/nueva_consulta.html")

@consulta_bp.route("/consulta/manage")
def gestionar_consulta():
    consultas = Consulta.query.all()

    return render_template("gestionar_consulta.html", consultas = consultas)

@consulta_bp.route("/consulta/delete/<int:id>", methods = ["POST"])
def eliminar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()

    flash("Consulta eliminada con éxito!")
    
    return redirect(url_for("consulta.gestionar_consulta"))

@consulta_bp.route("/consulta/edit/<int:id>", methods = ["GET", "POST"])
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

        return redirect(url_for("consulta.gestionar_consulta"))

    return render_template("editar_consulta.html", consulta=consulta)

@consulta_bp.route("/consulta/recent")
def consulta_dia():
    try:
        consultas = Consulta.query.order_by(Consulta.id.desc()).limit(5).all()
    except Exception as e:
        print(" Error cargando consultas:", e)
        consultas = []

    return render_template("dashboards/consultas/consulta_dia.html", consulta_dia = consultas)

@consulta_bp.route("/registro_medico/<int:consulta_id>", methods=['GET','POST'])
def registro_medico(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)
    if request.method == 'POST':
            examen = request.form['examen']
            diagnostico = request.form['diagnostico']
            tratamiento = request.form['tratamiento']
            recomendaciones = request.form['recomendaciones']
            ultima_consulta = Consulta.query.order_by(Consulta.id.desc()).first()

            if not ultima_consulta:
                flash("No hay ninguna consulta activa, primero agenda una.", "error")
                return redirect(url_for("consulta.consulta"))

            nuevo_registro = RegistroMedico(
                consulta_id=consulta_id,
                examen=examen,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                recomendaciones=recomendaciones
            )
            db.session.add(nuevo_registro)
            db.session.commit()
            flash("Registro médico guardado correctamente.", "success")
            return redirect(url_for('consulta.registro_medico', consulta_id=consulta.id))   
    registros = consulta.registros  
    return render_template("dashboards/consultas/registro_medico.html", consulta=consulta, registros=registros)



@consulta_bp.route("/api/consulta/<int:id>")
def get_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    data = {
        "id": consulta.id,
        "mascota": consulta.nombredemascota,
        "dueno": consulta.nombrededueno,
        "hora": consulta.hora,
        "veterinario": consulta.veterinario,
        "datos": consulta.datosdeconsulta,
        "registros": [
            {
                "examen": r.examen,
                "diagnostico": r.diagnostico,
                "tratamiento": r.tratamiento,
                "recomendaciones": r.recomendaciones
            } for r in consulta.registros
        ]
    }
    return jsonify(data)