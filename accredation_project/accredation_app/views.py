# views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import AccreditationApplication, Approval, get_approvals_needed, LocalMonitor, InternationalObserver
from .forms import AccreditationApplicationForm, UserRegisterForm, UserLoginForm, ApprovalForm,AccreditationApplicationLOForm, LocalMonitorRegistrationForm, InternationalMonitorRegistrationForm
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
from .pdf_utils import generate_certificate_with_watermark



###############################          START OF NEW VIEWS        ################################################

def view_local_cert(request, entry_id):
    # Fetch the LocalMonitor entry from the database
    local_monitor = LocalMonitor.objects.get(id=entry_id)

    # Convert LocalMonitor object to dictionary format
    local_monitor_data = {
        'institution_name': local_monitor.institution_name,
        'institution_abbreviation': local_monitor.institution_abbreviation,
        'institution_email': local_monitor.institution_email,
        'institution_address': local_monitor.institution_address,
        'contact_last_name': local_monitor.contact_last_name,
        'contact_other_names': local_monitor.contact_other_names,
        'contact_phone': local_monitor.contact_phone,
        'contact_email': local_monitor.contact_email,
        'contact_nrc_number': local_monitor.contact_nrc_number,
        'approval': local_monitor.get_approval_display(),  # Assuming you have choices for approval
        'created_on': local_monitor.created_on,
        'certificate_number': local_monitor.certificate_number,
    }

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Generate the PDF with actual data
    generate_certificate_with_watermark(local_monitor_data, buffer, 'C:/Users/Timothy/Desktop/PDF Samples/ecz_cert.png')

    # File pointer goes to the beginning of the buffer
    buffer.seek(0)

    # Return the PDF as a response for viewing in the browser
    return HttpResponse(buffer, content_type='application/pdf')

# Download PDF as a file
def download_local_cert(request, entry_id):
    # Fetch the LocalMonitor entry from the database
    local_monitor = get_object_or_404(LocalMonitor, id=entry_id)

    # Convert LocalMonitor object to dictionary format
    local_monitor_data = {
        'institution_name': local_monitor.institution_name,
        'institution_abbreviation': local_monitor.institution_abbreviation,
        'institution_email': local_monitor.institution_email,
        'institution_address': local_monitor.institution_address,
        'contact_last_name': local_monitor.contact_last_name,
        'contact_other_names': local_monitor.contact_other_names,
        'contact_phone': local_monitor.contact_phone,
        'contact_email': local_monitor.contact_email,
        'contact_nrc_number': local_monitor.contact_nrc_number,
        'approval': local_monitor.get_approval_display(),
        'created_on': local_monitor.created_on,
        'certificate_number': local_monitor.certificate_number,
    }

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Generate the PDF with actual data
    generate_certificate_with_watermark(local_monitor_data, buffer, 'C:/Users/Timothy/Desktop/PDF Samples/ecz_cert.png')

    # File pointer goes to the beginning of the buffer
    buffer.seek(0)

    # Create response to download the PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{local_monitor.institution_name}_{local_monitor.certificate_number}.pdf"'

    return response

def view_international_cert(request, entry_id):
    # Fetch the LocalMonitor entry from the database
    international_monitor = InternationalObserver.objects.get(id=entry_id)

    # Convert LocalMonitor object to dictionary format
    international_monitor_data = {
        'institution_name': international_monitor.institution_name,
        'institution_abbreviation': international_monitor.institution_abbreviation,
        'institution_email': international_monitor.institution_email,
        'institution_address': international_monitor.institution_address,
        'contact_last_name': international_monitor.contact_last_name,
        'contact_other_names': international_monitor.contact_other_names,
        'contact_phone': international_monitor.contact_phone,
        'contact_email': international_monitor.contact_email,
        'contact_nrc_number': international_monitor.contact_nrc_number,
        'approval': international_monitor.get_approval_display(),  # Assuming you have choices for approval
        'created_on': international_monitor.created_on,
        'certificate_number': international_monitor.certificate_number,
    }

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Generate the PDF with actual data
    generate_certificate_with_watermark(international_monitor_data, buffer, 'C:/Users/Timothy/Desktop/PDF Samples/ecz_cert.png')

    # File pointer goes to the beginning of the buffer
    buffer.seek(0)

    # Return the PDF as a response for viewing in the browser
    return HttpResponse(buffer, content_type='application/pdf')

# Download PDF as a file
def download_international_cert(request, entry_id):
    # Fetch the LocalMonitor entry from the database
    international_monitor = get_object_or_404(LocalMonitor, id=entry_id)

    # Convert LocalMonitor object to dictionary format
    international_monitor_data = {
        'institution_name': international_monitor.institution_name,
        'institution_abbreviation': international_monitor.institution_abbreviation,
        'institution_email': international_monitor.institution_email,
        'institution_address': international_monitor.institution_address,
        'contact_last_name': international_monitor.contact_last_name,
        'contact_other_names': international_monitor.contact_other_names,
        'contact_phone': international_monitor.contact_phone,
        'contact_email': international_monitor.contact_email,
        'contact_nrc_number': international_monitor.contact_nrc_number,
        'approval': international_monitor.get_approval_display(),
        'created_on': international_monitor.created_on,
        'certificate_number': international_monitor.certificate_number,
    }

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Generate the PDF with actual data
    generate_certificate_with_watermark(international_monitor_data, buffer, 'C:/Users/Timothy/Desktop/PDF Samples/ecz_cert.png')

    # File pointer goes to the beginning of the buffer
    buffer.seek(0)

    # Create response to download the PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{international_monitor.institution_name}_{international_monitor.certificate_number}.pdf"'

    return response

def local_registration(request):
    
    return render(request, 'local_registration.html')

def international_registration(request):
    return render(request, 'international_registration.html')


def local_form(request):
    if request.method == 'POST':
        form = LocalMonitorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            local_monitor = form.save(commit=False)  # Don't save to DB yet
            local_monitor.user = request.user  # Set the current user
            local_monitor.save()  # Now save to the DB
            return redirect('dashboard')  # Redirect to a success page
    else:
        form = LocalMonitorRegistrationForm()
        
    return render(request, 'local_form.html', {'form': form})

def international_form(request):
    if request.method == 'POST':
        form = InternationalMonitorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            international_monitor = form.save(commit=False)  # Don't save to DB yet
            international_monitor.user = request.user  # Set the current user
            international_monitor.save()  # Now save to the DB
            return redirect('dashboard')  # Redirect to a success page
    else:
        form = InternationalMonitorRegistrationForm()
        
    return render(request, 'international_form.html', {'form': form})


@login_required
def user_dashboard(request):
    local_applications = LocalMonitor.objects.filter(user=request.user)
    international_applications = InternationalObserver.objects.filter(user=request.user)


    context = {
        'local_applications': local_applications,
        'international_applications': international_applications,
    }
    return render(request, 'index.html', context)



###############################          END OF NEW VIEWS        ################################################




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

