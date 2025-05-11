from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import re

def generate_esg_pdf(org_record):
    name_clean = re.sub(r'\W+', '_', org_record['org_name'].lower()).strip("_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{org_record['org_id']}_{name_clean}_esg_report_{timestamp}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, f"📄 ESG Risk Report – {org_record['org_name']}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Organization ID: {org_record['org_id']}")
    c.drawString(50, height - 120, f"Sector: {org_record['sector']}")
    c.drawString(50, height - 140, f"Country: {org_record['country']}")
    c.drawString(50, height - 160, f"Report Date: {org_record['report_date']}")

    c.drawString(50, height - 200, f"Emissions Score: {org_record['emissions_score']}")
    c.drawString(50, height - 220, f"Labor Compliance Score: {org_record['labor_compliance_score']}")
    c.drawString(50, height - 240, f"Governance Index: {org_record['governance_index']}")

    c.setFont("Helvetica-Bold", 14)
    flag = "⚠️ High ESG Risk" if org_record['predicted_esg_flagged'] else "✅ Low ESG Risk"
    c.drawString(50, height - 280, f"Model Prediction: {flag}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 35, "This report was generated using an ML model trained on ESG scores.")

    c.save()
    return filename
