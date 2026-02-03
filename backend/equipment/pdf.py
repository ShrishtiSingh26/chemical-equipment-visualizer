from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import io

def generate_pdf(summary):
    buffer = io.BytesIO()
    # 1. Setup Document Template
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    # Custom Styles for UI-like look
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1a5f7a"),
        spaceAfter=20,
        alignment=1 
    )
    label_style = ParagraphStyle('LabelStyle', fontSize=10, textColor=colors.grey, alignment=1)
    value_style = ParagraphStyle('ValueStyle', fontSize=14, fontName='Helvetica-Bold', alignment=1)

    elements = []

    # --- SECTION 1: HEADER TITLE ---
    elements.append(Paragraph("Chemical Equipment Report", title_style))
    elements.append(Spacer(1, 12))

    # --- SECTION 2: SUMMARY CARDS (Table) ---
    card_data = [
        [Paragraph("Total Equipment", label_style), Paragraph("Avg Flowrate", label_style), 
         Paragraph("Avg Pressure", label_style), Paragraph("Avg Temp", label_style)],
        [Paragraph(str(summary.get('total_equipment', 0)), value_style),
         Paragraph(f"{summary.get('avg_flowrate', 0):.2f} L/min", value_style),
         Paragraph(f"{summary.get('avg_pressure', 0):.2f} psi", value_style),
         Paragraph(f"{summary.get('avg_temperature', 0):.2f} °C", value_style)]
    ]

    summary_table = Table(card_data, colWidths=[125, 125, 125, 125])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 30))

    # --- SECTION 3: VISUAL BAR CHART ---
    elements.append(Paragraph("Equipment Distribution Chart", styles['Heading2']))
    
    dist_data = summary.get('type_distribution', {})
    chart_values = [list(dist_data.values())] 
    chart_labels = list(dist_data.keys())

    # Drawing container for the chart
    d = Drawing(500, 200)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 400
    bc.data = chart_values
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.categoryNames = chart_labels
    bc.bars[0].fillColor = colors.HexColor("#1a5f7a") # Changed back to Blue to match Header
    
    d.add(bc)
    elements.append(d)
    elements.append(Spacer(1, 20))

    # --- SECTION 4: DATA TABLE ---
    elements.append(Paragraph("Detailed Type Distribution", styles['Heading2']))
    
    table_data = [["Equipment Type", "Count"]]
    for eq_type, count in dist_data.items():
        table_data.append([eq_type, count])

    dist_table = Table(table_data, colWidths=[350, 100])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a5f7a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#eeeeee")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")])
    ]))
    elements.append(dist_table)

    # 5. Build Final PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer