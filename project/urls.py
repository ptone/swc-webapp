import os

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django_browserid.views import Verify
from swc.views import UpcomingBootcamps, EventDetail, EditProfile, ProfileView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^people/(?P<pk>\d+)/edit/$',
        login_required(EditProfile.as_view()), name='profile_edit'),
    url(r'^people/(?P<pk>\d+)/',
        ProfileView.as_view(), name='profile_view'),
    url(r'^bootcamps/upcoming/', UpcomingBootcamps.as_view(),
        name='bootcamps_upcoming'),
    url(r'^bootcamps/(?P<pk>\d+)/(?P<slug>[-\w\d]+)', EventDetail.as_view(),
        name='event_detail'),
    url(r'^bootcamps/(?P<pk>\d+)/', EventDetail.as_view(),
        name='event_detail_id'),
    url(r'^accounts/login/', Verify.as_view(), name="login"),
    url(r'^admin/', include(admin.site.urls)),
    (r'^browserid/', include('django_browserid.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
)

if 'production' not in os.environ['DJANGO_SETTINGS_MODULE']:
    urlpatterns += staticfiles_urlpatterns()
