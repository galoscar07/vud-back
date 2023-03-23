from django.contrib import admin

from authentication.models import User, Clinic, Doctor, Document, ClinicReview, RequestToRedeemClinic

admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Document)
admin.site.register(ClinicReview)
admin.site.register(RequestToRedeemClinic)

# Register your models here.
