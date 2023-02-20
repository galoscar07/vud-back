from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from footerlabels import views

urlpatterns = [
    path('', views.FooterLabelList.as_view(), name=''),
    path('<int:pk>/', views.FooterLabelList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
