# accreditation_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class AccreditationType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# class AccreditationApplication(models.Model):
#     STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#     ]
#     institution_name = models.CharField(max_length=255)
#     contact_person = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     accreditation_type = models.CharField(max_length=25, default='International Observers')
#     address = models.TextField()
#     document = models.FileField(upload_to='documents/')
#     nrc_front = models.ImageField(upload_to='nrcs/')
#     nrc_back = models.ImageField(upload_to='nrcs/')
#     photo = models.ImageField(upload_to='photos/')
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='international_applications')
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.institution_name
    

# class AccreditationApplicationLO(models.Model):
#     STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#     ]
#     institution_name = models.CharField(max_length=255)
#     contact_person = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     accreditation_type = models.CharField(max_length=20, default='Local Observers')
#     address = models.TextField()
#     document = models.FileField(upload_to='documents/')
#     nrc_front = models.ImageField(upload_to='nrcs/')
#     nrc_back = models.ImageField(upload_to='nrcs/')
#     photo = models.ImageField(upload_to='photos/')
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='local_applications')
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.institution_name

class AccreditationApplication(models.Model):
    # Organization Details
    mofaic_clearance = models.FileField(upload_to='clearance/', help_text="Upload MOFAIC clearance document")
    
    # Observer Information
    estimated_observers = models.IntegerField(help_text="Enter estimated number of observers")
    observers_list = models.FileField(upload_to='observers_list/', help_text="Upload list of names of individual observers/monitors")
    
    # Sponsoring Institution Details
    sponsoring_institution_letter = models.FileField(upload_to='sponsoring_letters/', help_text="Upload introductory letter from sponsoring institution")

    # Observer Documents
    id_document = models.FileField(upload_to='id_documents/', help_text="Upload copies of national ID or Passport")
    passport_photo = models.FileField(upload_to='passport_photos/', help_text="Upload passport size photo (colour, correct dimensions)")
    
    # Stay Information
    city_town_district = models.CharField(max_length=255, help_text="Enter city/town/district of stay")
    hotel_facility = models.CharField(max_length=255, help_text="Enter hotel or lodging facility while in Zambia")
    duration_of_stay = models.CharField(max_length=100, help_text="Enter duration of stay in Zambia")
    
    # Observer Mission
    mission_statement = models.TextField(help_text="Provide summary of mission statement for observer activities")
    
    # New Fields
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', help_text="Application status")  # 1. Status field
    approval_date = models.DateField(null=True, blank=True, help_text="Date the application was approved")  # 2. Approval Date
    approver_name = models.CharField(max_length=255, null=True, blank=True, help_text="Name of the person who approved the application")  # 3. Approver Name
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='international_applications', help_text="User who created the application")  # 4. Created by field

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)  # Record creation time

    def __str__(self):
        return f"Application by {self.sponsoring_institution_letter}"

class AccreditationApplicationLO(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    institution_name = models.CharField(max_length=255)
    institution_abbreviation = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50)
    email = models.EmailField()
    physical_address = models.TextField()
    last_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    id_number_passport = models.CharField(max_length=50)
    head_of_institution_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    head_phone_number = models.CharField(max_length=20)
    organizational_registration = models.FileField(upload_to='documents/')
    introduction_letter = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='local_applications')
    created = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateField(null=True, blank=True)
    approver_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.institution_name

    
class Approval(models.Model):
    application = models.ForeignKey(AccreditationApplication, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

class ApprovalSetting(models.Model):
    required_approvals = models.IntegerField(default=1)

def get_approvals_needed():
    setting = ApprovalSetting.objects.first()
    if setting:
        return setting.required_approvals
    return 1
