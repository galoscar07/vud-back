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
    path('banners/', views.BannerCardList.as_view(), name='banners'),
    path('adds/', views.AddsCardList.as_view(), name='adds'),
    path('newsletter/', views.NewsletterView.as_view(), name='newsletter'),
    path('blogposts/', views.BlogPostListAPIView.as_view(), name='blogpost-list'),
    path('blogposts/<int:pk>/', views.BlogPostDetailAPIView.as_view(), name='blogpost-detail'),
    path('tags/', views.TagListAPIView.as_view(), name='tag-list'),
    path('send-message-clinic/', views.SendMessageClinic.as_view(), name='send-message-clinic'),
    path('clinics-list/', views.ClinicNamesListAPIView.as_view(), name='clinic-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
