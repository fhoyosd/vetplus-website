from flask import Blueprint, render_template, request, send_file
from vetplus.models import Order

import pdfkit
import io

informes_bp = Blueprint("informes", __name__)

@informes_bp.route("/informes")
def informes():
    return render_template("informes.html")

@informes_bp.route("/informes/manage")
def manage_informes():
    ventas = Order.query.all()
    return render_template("dashboards/informes/gestion_informes.html", ventas = ventas)

@informes_bp.route("/informes/generar_pdf", methods = ["POST"])
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

    pdf_file = io.BytesIO()
    pdfkit.from_string(html_completo, pdf_file)
    pdf_file.seek(0)

    return send_file(pdf_file, as_attachment = True, download_name = "venta.pdf", mimetype = 'application/pdf')