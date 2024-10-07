from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import pandas as pd
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import ttfonts
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

def generate_certificate_with_watermark(local_monitor, file_path, watermark_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    courier_regular = ttfonts.TTFont('Courier', "C:/Users/Timothy/Desktop/PDF Samples/Courier_Prime/CourierPrime-Regular.ttf")
    pdfmetrics.registerFont(courier_regular)

    courier_bold = ttfonts.TTFont('Courier-Bold', "C:/Users/Timothy/Desktop/PDF Samples/Courier_Prime/CourierPrime-Bold.ttf")
    pdfmetrics.registerFont(courier_regular)

    merriweather_regular = ttfonts.TTFont('Merriweather', "C:/Users/Timothy/Desktop/PDF Samples/Merriweather/Merriweather-Regular.ttf")
    pdfmetrics.registerFont(merriweather_regular)

    merriweather_bold = ttfonts.TTFont('Merriweather-Bold', "C:/Users/Timothy/Desktop/PDF Samples/Merriweather/Merriweather-Bold.ttf")
    pdfmetrics.registerFont(merriweather_bold)

    # Set transparency (alpha value) for the watermark
    c.saveState()  # Save the current graphics state
    c.setFillAlpha(1.0)  # Set transparency level (1.0 is opaque, 0.0 is fully transparent)

    # Add watermark image at the center of the page
    watermark_width = width  # Adjust the size of the watermark image (width)
    watermark_height = height  # Adjust the size of the watermark image (height)
    
    # Calculate position for centering
    x_position = (width - watermark_width) / 2
    y_position = (height - watermark_height) / 2

    # Draw the watermark (optional transparency can be set using c.setFillAlpha if needed)
    c.drawImage(watermark_path, x_position, y_position, width=watermark_width, height=watermark_height, mask='auto')

    # Main Certificate Border
    c.setStrokeColor(colors.darkorange)
    c.setLineWidth(2)
    
    # Main Border Rectangle
    border_margin = 10
    c.rect(border_margin, border_margin, width - 2 * border_margin, height - 2 * border_margin)
   

    # Title
    c.setFont("Merriweather-Bold", 18)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 145, "THE ELECTORAL COMMISSION OF ZAMBIA")

     # Institution Address (Left-aligned)
    c.setFont("Helvetica", 16)
    c.drawString(225, height - 250, "THIS CERTIFIES THAT")

    # Institution Name (Centering it)
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.green)
    c.drawCentredString(width / 2, height - 335, local_monitor['institution_name'])

    
    
    # Contact Person (Centered text)
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 420, f"represented by {local_monitor['contact_other_names']} {local_monitor['contact_last_name']},")
    c.drawCentredString(width / 2, height - 440, "has been accredited by our organization")
    c.drawCentredString(width / 2, height - 460, "as a Local Observer")

    # Approval Status (Centered)
    c.setFont("Helvetica-Bold", 20)
    approval_status = local_monitor['approval'].capitalize()
    c.drawCentredString(width / 2, height - 550, f"{approval_status}")
    
    # Footer Signature
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 80, "_______________________")
    c.drawString(60, 60, "Mwangala Zaloumis")
    c.setFont("Helvetica", 10)
    c.drawString(90, 45, "Chairperson")

    signature_image = "C:/Users/Timothy/Desktop/PDF Samples/sig.png"  # Load the signature image
    c.drawImage(signature_image, 65, 80, width=100, height=30, mask='auto')  # Adjust the position and size

    # Certificate number in red
    certificate_number = local_monitor['certificate_number']
    c.setFont("Courier-Bold", 12)
    c.setFillColor(colors.red)
    c.drawCentredString(width - 120, 75, f"Certificate No: {certificate_number}")

    # Issue Date
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(width - 200, 60, f"Issue Date: {local_monitor['created_on'].strftime('%Y-%m-%d %H:%M:%S')}")

    # Save the PDF
    c.showPage()
    c.save()