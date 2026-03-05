from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

DATA_DIR = "../data/pdfs"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

pdf_path = os.path.join(DATA_DIR, "Hydraulic_System_Manual.pdf")

c = canvas.Canvas(pdf_path, pagesize=letter)
c.setFont("Helvetica-Bold", 16)
c.drawString(100, 750, "Hydraulic System Maintenance & Troubleshooting Manual")
c.setFont("Helvetica", 12)
c.drawString(100, 730, "Model: H-2000 Series")
c.drawString(100, 715, "Manufacturer: Antigravity Hydraulics")

c.setFont("Helvetica-Bold", 14)
c.drawString(100, 680, "Chapter 1: Troubleshooting Common Faults")

c.setFont("Helvetica-Bold", 12)
c.drawString(100, 650, "Symptom: Pump making loud cavitating noise")
c.setFont("Helvetica", 12)
c.drawString(100, 635, "Possible Cause 1: Low oil level in reservoir.")
c.drawString(100, 620, "Remedy: Check sight glass. Refill with ISO VG 46 oil to upper mark.")
c.drawString(100, 605, "Possible Cause 2: Clogged suction strainer.")
c.drawString(100, 590, "Remedy: Remove strainer and clean with solvent. Replace if damaged.")
c.drawString(100, 575, "Possible Cause 3: Air leak in suction line.")
c.drawString(100, 560, "Remedy: Tighten all flange bolts on suction line. Replace O-rings.")

c.setFont("Helvetica-Bold", 12)
c.drawString(100, 530, "Symptom: System pressure fluctuates randomly")
c.setFont("Helvetica", 12)
c.drawString(100, 515, "Possible Cause: Accumulator pre-charge lost.")
c.drawString(100, 500, "Remedy: Check nitrogen pre-charge. It should be 80% of operating pressure.")
c.drawString(100, 485, "Possible Cause: Stick-slip in relief valve.")
c.drawString(100, 470, "Remedy: Inspect pilot stage of relief valve for contaminants.")

c.setFont("Helvetica-Bold", 12)
c.drawString(100, 440, "Symptom: Cylinder extends but will not retract")
c.setFont("Helvetica", 12)
c.drawString(100, 425, "Possible Cause: Directional valve solenoid failure.")
c.drawString(100, 410, "Remedy: Check voltage at coil B. If 0V, check PLC output.")
c.drawString(100, 395, "Possible Cause: Pilot check valve jammed.")
c.drawString(100, 380, "Remedy: Disassemble and clean check valve.")

c.save()
print(f"Created dummy manual at {pdf_path}")
