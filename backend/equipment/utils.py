import io
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
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
