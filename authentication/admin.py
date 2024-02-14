from django.contrib import admin

from authentication.models import User, Clinic, CollaboratorDoctor, Document, ClinicReview, RequestToRedeemClinic, \
    DoctorReview, RequestToRedeemDoctor


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)


class DoctorAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)


class ClinicAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(CollaboratorDoctor, DoctorAdmin)
admin.site.register(Document)
admin.site.register(ClinicReview)
admin.site.register(DoctorReview)
admin.site.register(RequestToRedeemClinic)
admin.site.register(RequestToRedeemDoctor)

# Register your models here.
