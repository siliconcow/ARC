from django.conf.urls import patterns, include, url
from django.conf import settings
from ajax_select import urls as ajax_select_urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import arc.models
import arc.views
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
      url(r'^$', 'arc.views.home', name='home'),
    # url(r'^arc/', include('arc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^accounts/login/$', 'django.contrib.auth.views.login'),
     (r'^lookups/', include(ajax_select_urls)),
     url(r'^admin/', include(admin.site.urls)),
     (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
                }),
            )
