# views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import AccreditationApplication, Approval, get_approvals_needed
from .forms import AccreditationApplicationForm, UserRegisterForm, UserLoginForm, ApprovalForm,AccreditationApplicationLOForm
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import logging
import os
from io import BytesIO
import io
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, green
from reportlab.pdfgen import canvas
from django.http import HttpResponse, FileResponse
from reportlab.lib.enums import TA_CENTER 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PyPDF2 import PdfReader, PdfWriter 
from .models import AccreditationApplication, AccreditationApplicationLO
# from django.template.loader import render_to_string
# from weasyprint import HTML

logger = logging.getLogger(__name__)
def homepage(request):
    return render(request, 'loginpage.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard or another page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    if request.method == 'POST':
        auth_logout(request)
        logger.info(f"User {request.user.username} logged out.")
        return redirect('/')
    return render(request, 'logout.html')

@login_required
@staff_member_required
def applications_list(request):
    applications = AccreditationApplication.objects.all()
    return render(request, 'applications_list.html', {'applications': applications})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def application_success(request):
    return render(request, 'application_success.html')


@login_required
def application_form(request):
    if request.method == 'POST':
        form = AccreditationApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.created_by = request.user
            application.save()
            return redirect('application_success')
    else:
        form = AccreditationApplicationForm()
    context = {'form': form}
    return render(request, 'application_form.html', context)

@login_required
def application_lo_form(request):
    if request.method == 'POST':
        form = AccreditationApplicationLOForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.created_by = request.user
            application.save()
            return redirect('application_success')
    else:
        form = AccreditationApplicationLOForm()
    context = {'form': form}
    return render(request, 'application_form_LO.html', context)

@staff_member_required
def manage_applications(request):
    applications = AccreditationApplication.objects.filter(status='pending')
    return render(request, 'manage_applications.html', {'applications': applications})

@staff_member_required
def approve_application(request, application_id):
    application = get_object_or_404(AccreditationApplication, id=application_id)
    application.status = 'APPROVED'
    application.save()
    return redirect('manage_applications')

@staff_member_required
def reject_application(request, application_id):
    application = get_object_or_404(AccreditationApplication, id=application_id)
    application.status = 'REJECTED'
    application.save()
    return redirect('manage_applications')

@login_required
def user_dashboard(request):
    local_applications = AccreditationApplicationLO.objects.filter(created_by=request.user)
    international_applications = AccreditationApplication.objects.filter(created_by=request.user)

    context = {
        'local_applications': local_applications,
        'international_applications': international_applications,
    }
    return render(request, 'index.html', context)

# @login_required

# def download_certificate(request, application_id):
#      # Try to fetch the application from both models
#     application = get_object_or_404(AccreditationApplication, id=application_id)
#     local_application = None

#     if not application:
#         local_application = get_object_or_404(AccreditationApplicationLO, id=application_id)

#     # Prepare context based on which application is found
#     context = {
#         'application': application,
#         'local_application': local_application,
#     }

#     # Render the template with application data
#     html_string = render_to_string('certificate_template.html', {'application': application})
#     html = HTML(string=html_string)

#     # Generate PDF
#     pdf = html.write_pdf()

#     # Return as HTTP response
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="certificate_{application_id}.pdf"'
#     return response
# # def download_certificate(request, application_id):
#     application = get_object_or_404(AccreditationApplication, pk=application_id)

#     # Create a file-like buffer to receive PDF data
#     buffer = BytesIO()

#     # Create the PDF object using ReportLab's SimpleDocTemplate
#     doc = SimpleDocTemplate(buffer, pagesize=letter)

#     # Define styles for the certificate
#     title_style = ParagraphStyle(
#         'Title',
#         fontSize=24,
#         spaceAfter=20,
#         textColor=HexColor('#029053')  # Primary Color: Dark Green
#     )

#     centered_style = ParagraphStyle(
#         'CenteredStyle',
#         parent=title_style,
#         alignment=1  # 1 is for center alignment
#     )

#     normal_style = ParagraphStyle(
#          'CenteredStyle',
#         fontSize=12,
#         spaceAfter=10,
#         textColor=HexColor('#000000'),  # Default text color (black)
#         alignment=1 # 1 is for center alignment
#     )

#     # Function to draw the logo on the canvas
#     def draw_logo(canvas, doc):
#         logo_path = 'C:/dev/accreditation/static/img/logo.png'
#         canvas.saveState()
#         canvas.drawImage(logo_path, (doc.width - 4 * inch) / 2, doc.height + 0.5 * inch, width=4 * inch, height=1 * inch, preserveAspectRatio=True, anchor='n')
#         canvas.restoreState()

#     # Function to draw the address below the top logo
#     def draw_address(canvas, doc):
#         address_text = "Elections House, Haile Selassie Avenue, Longacres, P.O Box 50274, 10101 Lusaka, Zambia."
#         canvas.setFont("Helvetica", 10)
#         canvas.drawCentredString(doc.width / 2, doc.height - 0.75 * inch, address_text)

#     # Function to draw social media links
#     def draw_socials(canvas, doc):
#         # Define the positions and styles for social media icons and handles
#         social_x = 1 * inch
#         social_y = 0.75 * inch
#         icon_size = 0.5 * inch

#         # Facebook
#         facebook_logo = 'C:/dev/accreditation/static/img/facebook.png'
#         canvas.drawImage(facebook_logo, social_x, social_y, width=icon_size, height=icon_size)
#         canvas.setFont("Helvetica", 10)
#         canvas.drawString(social_x + icon_size + 0.1 * inch, social_y + 0.1 * inch, "Facebook")

#         # Twitter
#         twitter_logo = 'C:/dev/accreditation/static/img/twitter.png'
#         canvas.drawImage(twitter_logo, social_x + 2 * inch, social_y, width=icon_size, height=icon_size)
#         canvas.setFont("Helvetica", 10)
#         canvas.drawString(social_x + 2 * inch + icon_size + 0.1 * inch, social_y + 0.1 * inch, "Twitter")

#         # Instagram
#         instagram_logo = 'C:/dev/accreditation/static/img/instagram.png'
#         canvas.drawImage(instagram_logo, social_x + 4 * inch, social_y, width=icon_size, height=icon_size)
#         canvas.setFont("Helvetica", 10)
#         canvas.drawString(social_x + 4 * inch + icon_size + 0.1 * inch, social_y + 0.1 * inch, "Instagram")

#     # Function to draw the watermark logo
#     def draw_watermark(canvas, doc):
#         watermark_path = 'C:/dev/accreditation/static/accreditation_app/img/watermark_logo.png'
#         canvas.saveState()
#         canvas.setFillAlpha(0.5)  # Set transparency for watermark
#         canvas.drawImage(watermark_path, (doc.width - 6 * inch) / 2, (doc.height - 8 * inch) / 2, width=6 * inch, height=8 * inch, preserveAspectRatio=True, anchor='c')
#         canvas.restoreState()

#     # Function to draw the green line above the social media links
#     def draw_green_line(canvas, doc):
#         canvas.setStrokeColor(green)
#         canvas.setLineWidth(2)
#         canvas.line(0.5 * inch, 1 * inch, doc.width - 0.5 * inch, 1 * inch)

#     # Composite function to draw all elements on the page
#     def draw_elements(canvas, doc):
#         draw_watermark(canvas, doc)
#         draw_logo(canvas, doc)
#         draw_address(canvas, doc)
#         draw_green_line(canvas, doc)
#         draw_socials(canvas, doc)

#     # Build the PDF content
#     elements = []

#     elements.append(Paragraph('Electoral Commission of Zambia (ECZ)', title_style))
#     elements.append(Spacer(1, 0.25 * inch))
#     elements.append(Paragraph('Certificate of Accreditation', centered_style))
#     elements.append(Spacer(1, 0.5 * inch))

#     # Content with specific formatting as separate paragraphs
#     content_lines = [
#         f"This is to certify that",
#         f"{application.contact_person}",
#         f"is accredited as {application.accreditation_type.name}",
#         f" Representative for {application.institution_name}",
#         f"during the 2026",
#         f"General elections."
#     ]

#     # Add each line as a separate paragraph with normal style
#     for line in content_lines:
#         elements.append(Paragraph(line, normal_style))
#         elements.append(Spacer(1, 0.1 * inch))  # Optional spacer for line spacing

#     # Add elements to the PDF document
#     doc.build(elements, onFirstPage=draw_elements, onLaterPages=draw_elements)

#     # Move to the beginning of the buffer to start reading
#     buffer.seek(0)

#     # Prepare the HTTP response
#     response = HttpResponse(content_type='application/pdf')
#     file_name = f"certificate_{application.accreditation_type.name}_{application_id}.pdf"
#     response['Content-Disposition'] = f'attachment; filename="{file_name}"'

#     # Write the PDF content to the response
#     response.write(buffer.getvalue())
#     return response

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
     # Fetch all applications
    accreditation_applications = AccreditationApplication.objects.all()
    accreditation_lo_applications = AccreditationApplicationLO.objects.all()

    # Combine applications or pass separately as context
    context = {
        'accreditation_applications': accreditation_applications,
        'accreditation_lo_applications': accreditation_lo_applications,
    }

    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def view_application(request, application_id=None):
    application = None
    local_application = None

    # Try fetching from AccreditationApplication
    if application_id:
        application = AccreditationApplication.objects.filter(id=application_id).first()

    # Try fetching from AccreditationApplicationLO if it's a local application
    if not application:
        local_application = AccreditationApplicationLO.objects.filter(id=application_id).first()

    context = {
        'application': application,
        'local_application': local_application,
    }
    return render(request, 'view_application.html', context)

@login_required
@user_passes_test(is_admin)
def approve_application(request, application_id):
    application = get_object_or_404(AccreditationApplication, id=application_id)
    Approval.objects.create(application=application, approved_by=request.user)
    approvals_needed = get_approvals_needed()
    if application.approval_set.count() >= approvals_needed:
        application.status = 'approved'
        application.save()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def reject_application(request, application_id):
    application = get_object_or_404(AccreditationApplication, id=application_id)
    application.status = 'rejected'
    application.save()
    return redirect('admin_dashboard')

# @login_required
# @user_passes_test(is_admin)
# def download_application(request, application_id):
#     application = get_object_or_404(AccreditationApplication, id=application_id)
#     buffer = generate_application_pdf(application)
#     return FileResponse(buffer, as_attachment=True, filename=f"{application.institution_name}_{application.accreditation_type}_application.pdf")

# def generate_application_pdf(application):
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()

#     elements = []
#     elements.append(Paragraph('Accreditation Application', styles['Title']))
#     elements.append(Spacer(1, 12))
    
#     elements.append(Paragraph(f'Institution Name: {application.institution_name}', styles['Normal']))
#     elements.append(Paragraph(f'Contact Person: {application.contact_person}', styles['Normal']))
#     elements.append(Paragraph(f'Email: {application.email}', styles['Normal']))
#     elements.append(Paragraph(f'Phone: {application.phone}', styles['Normal']))
#     elements.append(Paragraph(f'Accreditation Type: {application.accreditation_type}', styles['Normal']))
#     elements.append(Paragraph(f'Address: {application.address}', styles['Normal']))

#     doc.build(elements)
#     buffer.seek(0)

#     return buffer