from django.contrib import admin

from authentication.models import User, Clinic, CollaboratorDoctor, Document, ClinicReview, RequestToRedeemClinic, \
    DoctorReview, RequestToRedeemDoctor

admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(CollaboratorDoctor)
admin.site.register(Document)
admin.site.register(ClinicReview)
admin.site.register(DoctorReview)
admin.site.register(RequestToRedeemClinic)
admin.site.register(RequestToRedeemDoctor)

# Register your models here.
