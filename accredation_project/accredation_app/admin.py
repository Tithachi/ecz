from django.contrib import admin
from .models import AccreditationApplication, AccreditationType, Approval, ApprovalSetting

# admin.site.register(AccreditationApplication)
admin.site.register(AccreditationType)
admin.site.register(Approval)
admin.site.register(ApprovalSetting)
class AccreditationApplicationAdmin(admin.ModelAdmin):
    list_display = ('sponsoring_institution_letter', 'status', 'approval_date', 'approver_name', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('sponsoring_institution_letter', 'approver_name')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Automatically set the creator for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(AccreditationApplication, AccreditationApplicationAdmin)
# Register your models here.
