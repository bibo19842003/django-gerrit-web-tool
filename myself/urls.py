from django.urls import path

from . import views

urlpatterns = [
    path('infor_list/', views.infor_list),
]
