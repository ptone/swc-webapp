import os

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from swc.views import (UpcomingBootcamps, EventDetail, EditProfile,
        ProfileView, AddTimeChunk, DeleteTimeChunk)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^profile/edit/$',
        login_required(EditProfile.as_view()), name='profile_edit'),

    url(r'^profile/(?P<pk>\d+)/',
        ProfileView.as_view(), name='profile_view'),

    url(r'^profile/$',
        ProfileView.as_view(), name='profile_view_user'),

    url(r'^profile/calendar/$', 'swc.views.calendar'),

    url(r'^bootcamps/upcoming/', UpcomingBootcamps.as_view(),
        name='bootcamps_upcoming'),

    url(r'^bootcamps/(?P<pk>\d+)/(?P<slug>[-\w\d]+)', EventDetail.as_view(),
        name='event_detail'),

    url(r'^bootcamps/(?P<pk>\d+)/', EventDetail.as_view(),
        name='event_detail_id'),

    url(r'^dates/add/$', AddTimeChunk.as_view(), name='dates_add'),

    url(r'^dates/delete/$', DeleteTimeChunk.as_view(), name='dates_delete'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        name='logout'),

    url(r'^manage/', include(admin.site.urls)),

    url(r'', include('social_auth.urls')),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
)

if 'production' not in os.environ['DJANGO_SETTINGS_MODULE']:
    urlpatterns += staticfiles_urlpatterns()
