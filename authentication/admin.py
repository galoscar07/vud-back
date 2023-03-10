from django.contrib import admin

from authentication.models import User, Clinic, Doctor, Document, ClinicReview

admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Document)
admin.site.register(ClinicReview)

# Register your models here.
