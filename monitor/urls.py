from django.urls import path

from . import views

urlpatterns = [
    path('m_cpu/', views.m_cpu),
    path('m_mem/', views.m_mem),
]
