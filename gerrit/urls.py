from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index),
    path('ct_m_p/', views.ct_m_p),
    path('ct_l_p/', views.ct_l_p),
    path('g_r/', views.g_r),
    path('g_r_log/', views.g_r_log),
    path('c_b/', views.c_b),
    path('c_b_log/', views.c_b_log),
    path('q_b/', views.q_b),
    path('g_c/', views.g_c),
    path('g_c_log/', views.g_c_log),
    path('p_c/', views.p_c),
    path('u_g/', views.u_g),
    path('g_t/', views.g_t),
    path('c_p/', views.c_p),
    path('c_p_log/', views.c_p_log),
]
