from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from footerlabels import views

urlpatterns = [
    path('footer/', views.FooterLabelList.as_view(), name='footer-labels'),
    path('medical-unity-types/', views.MedicalUnityTypesList.as_view(), name='medical-unity-types'),
    path('academic-degrees/', views.AcademicDegreeList.as_view(), name='academic-degrees'),
    path('specialities/', views.SpecialityList.as_view(), name='specialities'),
    path('competences/', views.MedicalSkillsList.as_view(), name='competences'),
    path('clinic-specialities/', views.ClinicSpecialitiesList.as_view(), name='clinic-specialities'),
    path('medical-facilities/', views.MedicalFacilitiesList.as_view(), name='medical-facilities'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
