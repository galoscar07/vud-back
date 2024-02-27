from django.contrib import admin

from authentication.models import User, Clinic, CollaboratorDoctor, Document, ClinicReview, RequestToRedeemClinic, \
    DoctorReview, RequestToRedeemDoctor


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)


class DoctorAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)


class ClinicAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)

class MyClinic(Clinic):
    class Meta:
        proxy = True
        verbose_name = "Clinici De Aprobat"


class MyDoctors(CollaboratorDoctor):
    class Meta:
        proxy = True
        verbose_name = "Doctori De Aprobat"


class CustomAdminClinic(admin.ModelAdmin):
    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)

        # Filter the queryset based on your criteria
        filtered_queryset = queryset.filter(is_visible=False, user__isnull=False)

        return filtered_queryset

class CustomAdminDoctor(admin.ModelAdmin):
    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)

        # Filter the queryset based on your criteria
        filtered_queryset = queryset.filter(is_visible=False, user__isnull=False)

        return filtered_queryset


# Register the model with the custom admin view
admin.site.register(User, UserAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(MyClinic, CustomAdminClinic)
admin.site.register(CollaboratorDoctor, DoctorAdmin)
admin.site.register(MyDoctors, CustomAdminDoctor)
admin.site.register(Document)
admin.site.register(ClinicReview)
admin.site.register(DoctorReview)
admin.site.register(RequestToRedeemClinic)
admin.site.register(RequestToRedeemDoctor)

# Register your models here.
