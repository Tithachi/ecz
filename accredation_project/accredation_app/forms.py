# accredation_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import AccreditationApplication,AccreditationType, AccreditationApplicationLO, LocalMonitor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


###############################          START OF NEW FORMS        ################################################

class LocalMonitorRegistrationForm(forms.ModelForm):
    class Meta:
        model = LocalMonitor
        fields = [
            'institution_name',
            'institution_abbreviation',
            'institution_email',
            'institution_address',
            'contact_last_name',
            'contact_other_names',
            'contact_phone',
            'contact_email',
            'contact_nrc_number',
            'head_full_name',
            'head_designation',
            'head_phone',
            'certificate_of_registration',
            'estimated_number_of_monitors',
            'monitors_list',
            'introductory_letter',
            'identification_docs',
            'passport_photo',
            'reason_for_application',
            'physical_address',
        ]


###############################          START OF NEW FORMS        ################################################



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AccreditationApplicationForm(forms.ModelForm):
    class Meta:
        model = AccreditationApplication
        fields = [
            'mofaic_clearance',
            'estimated_observers',
            'observers_list',
            'sponsoring_institution_letter',
            'id_document',
            'passport_photo',
            'city_town_district',
            'hotel_facility',
            'duration_of_stay',
            'mission_statement',
            # 'status', 'approval_date', 'approver_name', 'created_by'  # Optional for admin use
        ]
        
        widgets = {
            'estimated_observers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'city_town_district': forms.TextInput(attrs={'class': 'form-control'}),
            'hotel_facility': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_of_stay': forms.TextInput(attrs={'class': 'form-control'}),
            'mission_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizing file input fields (adding Bootstrap classes, etc.)
        self.fields['mofaic_clearance'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['observers_list'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['sponsoring_institution_letter'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['id_document'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['passport_photo'].widget.attrs.update({'class': 'form-control-file'})

class AccreditationApplicationLOForm(forms.ModelForm):
    class Meta:
        model = AccreditationApplicationLO
        fields = [
            'institution_name', 'institution_abbreviation', 'registration_number', 'email', 'physical_address',
            'last_name', 'other_names', 'phone', 'id_number_passport', 'head_of_institution_name', 'designation',
            'head_phone_number', 'organizational_registration', 'introduction_letter'
        ]

    def __init__(self, *args, **kwargs):
        super(AccreditationApplicationLOForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Application'))
         # Adjust queryset for accreditation_type field if needed
        # self.fields['accreditation_type'].queryset = AccreditationType.objects.all()

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = AccreditationApplication
        fields = ['status']
