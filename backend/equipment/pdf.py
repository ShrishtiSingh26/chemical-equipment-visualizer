from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_pdf(summary):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.drawString(50, 800, "Chemical Equipment Report")

    y = 760
    for key, value in summary.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
