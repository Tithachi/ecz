from django.contrib import admin
from .models import InternationalObserver, LocalMonitor

# Admin configuration for InternationalObserver
@admin.register(InternationalObserver)
class InternationalObserverAdmin(admin.ModelAdmin):
    list_display = (
        'institution_name', 
        'institution_abbreviation', 
        'institution_email', 
        'country_of_origin', 
        'duration_of_stay',
        'head_full_name', 
        'head_designation'
    )
    search_fields = ('institution_name', 'institution_abbreviation', 'country_of_origin')
    list_filter = ('country_of_origin', 'created_on', 'approval')
    readonly_fields = ('observers_list', 'organization_clearance', 'introductory_letter', 'identification_docs', 'passport_photo')

# Admin configuration for LocalMonitor
@admin.register(LocalMonitor)
class LocalMonitorAdmin(admin.ModelAdmin):
    list_display = (
        'institution_name', 
        'institution_abbreviation', 
        'institution_email', 
        'head_full_name', 
        'head_designation', 
        'estimated_number_of_monitors'
    )
    search_fields = ('institution_name', 'institution_abbreviation', 'head_full_name')
    list_filter = ('created_on', 'approval')
    readonly_fields = ('monitors_list', 'certificate_of_registration', 'introductory_letter', 'identification_docs', 'passport_photo')