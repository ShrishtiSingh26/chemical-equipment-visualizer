import io
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def analyze_csv(file):
    df = pd.read_csv(file)

    return {
        "total_equipment": len(df),
        "avg_flowrate": df["Flowrate"].mean(),
        "avg_pressure": df["Pressure"].mean(),
        "avg_temperature": df["Temperature"].mean(),
        "type_distribution": df["Type"].value_counts().to_dict()
    }


def generate_pdf(summary):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Chemical Equipment Report")
    y -= 40

    p.setFont("Helvetica", 11)

    # Text summary
    for key, value in summary.items():
        if key == "type_distribution":
            continue

        if y < 50:
            p.showPage()
            y = height - 50

        p.drawString(50, y, f"{key}: {value}")
        y -= 20

    # Chart
    if "type_distribution" in summary:
        labels = list(summary["type_distribution"].keys())
        values = list(summary["type_distribution"].values())

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_title("Equipment Type Distribution")
        plt.xticks(rotation=45)

        img_buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img_buffer, format="PNG")
        plt.close(fig)
        img_buffer.seek(0)

        p.showPage()
        p.drawImage(
            ImageReader(img_buffer),
            50,
            200,
            width=500,
            height=400
        )

    p.save()
    buffer.seek(0)
    return buffer


def password_protect_pdf(input_buffer, password):
    reader = PdfReader(input_buffer)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output
