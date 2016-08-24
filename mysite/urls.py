from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views

# compatible 1.6, from 1.7 it can auto load
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', views.login, {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', views.logout_then_login),

    url(r'^$', 'gerrit.views.index'),
    url(r'^index/$', 'gerrit.views.index'),
    url(r'^ct_m_p/$', 'gerrit.views.ct_m_p'),
    url(r'^ct_l_p/$', 'gerrit.views.ct_l_p'),
    url(r'^g_r/$', 'gerrit.views.g_r'),
    url(r'^g_r_log/$', 'gerrit.views.g_r_log'),
    url(r'^c_b/$', 'gerrit.views.c_b'),
    url(r'^c_b_log/$', 'gerrit.views.c_b_log'),
    url(r'^q_b/$', 'gerrit.views.q_b'),
    url(r'^g_c/$', 'gerrit.views.g_c'),
    url(r'^g_c_log/$', 'gerrit.views.g_c_log'),
)
