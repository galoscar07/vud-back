from django.contrib import admin

from authentication.models import User, Clinic, Doctor, Document

admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Document)

# Register your models here.
