from django.contrib import admin

from footerlabels.models import Footerlabels, MedicalUnityTypes, AcademicDegree, Speciality, MedicalSkills, \
    ClinicSpecialities, MedicalFacilities

admin.site.register(Footerlabels)
admin.site.register(MedicalUnityTypes)
admin.site.register(AcademicDegree)
admin.site.register(Speciality)
admin.site.register(MedicalSkills)
admin.site.register(ClinicSpecialities)
admin.site.register(MedicalFacilities)
