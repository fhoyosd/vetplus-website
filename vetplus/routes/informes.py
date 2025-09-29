from flask import Blueprint, render_template, request, send_file, jsonify
from vetplus.models import Order, Consulta

import pdfkit
import io

informes_bp = Blueprint("informes", __name__)


@informes_bp.route("/informes/manage")
def manage_informes():
    ventas = Order.query.all()
    consultas = Consulta.query.all()
    return render_template("dashboards/informes/gestion_informes.html",
                           ventas=ventas, consultas=consultas)

@informes_bp.route("/informes/generar_pdf", methods=["POST"])
def generar_pdf():
    html_fragment = request.json.get("html", "")

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #4d8ea1; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #000; padding: 8px; text-align: left; }}
            th {{ background-color: #4d8ea1; color: white; }}
        </style>
    </head>
    <body>
        {html_fragment}
    </body>
    </html>
    """

    # pdfkit devuelve bytes si le pones False
    pdf_bytes = pdfkit.from_string(html_completo, False)
    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="informe.pdf",
        mimetype="application/pdf"
    )