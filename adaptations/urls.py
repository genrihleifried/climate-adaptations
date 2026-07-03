from django.urls import path
from . import views

urlpatterns = [
    path('', views.adaptation_list, name='adaptation_list'),
    path('upload/', views.upload_csv, name='upload_csv'),
]