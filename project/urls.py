from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin

from swc.views import UpcomingBootcamps

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^bootcamps/upcoming/', UpcomingBootcamps.as_view(), name='upcoming_bootcamps'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^browserid/', include('django_browserid.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
)
