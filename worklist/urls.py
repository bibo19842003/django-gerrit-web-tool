from django.urls import path

from . import views

urlpatterns = [
    path('list_query/', views.list_query),
    path('list_create/', views.list_create),
    path('list_handle/', views.list_handle),
]
