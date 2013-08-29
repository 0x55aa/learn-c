from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'learnc.views.home', name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    # url(r'^learnc/', include('learnc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^step/', include('stepbystep.urls')),
    url(r'^exercise/', include('exercise.urls')),
    url(r'^commtents/', include('django.contrib.comments.urls')),
)
