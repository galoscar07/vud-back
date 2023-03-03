from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from footerlabels import views

urlpatterns = [
    path('footer', views.FooterLabelList.as_view(), name='footer-labels'),
    path('medical-unity-types', views.MedicalUnityTypesList.as_view(), name='medical-unity-types'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
