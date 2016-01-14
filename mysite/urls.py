from django.conf.urls import patterns, include, url
from django.contrib import admin

# compatible 1.6, from 1.7 it can auto load
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'gerrit.views.index'),
    url(r'^index/$', 'gerrit.views.index'),
    url(r'^ct_m_p/$', 'gerrit.views.ct_m_p'),
    url(r'^ct_l_p/$', 'gerrit.views.ct_l_p'),
)
