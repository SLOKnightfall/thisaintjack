#from django.conf.urls import patterns, include, url
from django.conf.urls import url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from campmanager import views, group, user, area

#urlpatterns = patterns('',
urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'', include('social_auth.urls')),
    url(r'', include('social_django.urls', namespace='social')),

    url(r'^$', views.index, name='index'),
    url(r'^burners/$', views.burnerlist, name='burnerlist'),
    url(r'^bigstuff/$', views.bigstufflist, name='bigstufflist'),

    url(r'^subcamp/(?P<subcamp>[^/]+)/$', views.subcamp, name='bigstufflist'),
    url(r'^group/(?P<siteid>[^/]+)/$', group.group, name='group'),
    url(r'^group/(?P<siteid>[^/]+)/bigstuff/(?P<stuffid>\d+)/$', area.area, name='area'),

    url(r'^user/newlogin/$', user.newlogin, name = 'newlogin'),
    url(r'^user/profile/(?P<username>[\w\s\.-]+)/$', user.profile, name= 'profile'),
    url(r'^user/profile/$', user.myprofile, name = 'myprofile'),
    url(r'^user/login/$', user.login, name = 'login'),
    url(r'^user/logout/$', user.logoff, name = 'logoff'),
    url(r'^user/login_error/', user.login_error, name = 'login_error'),
    url(r'^user/login_created/', user.login_created, name = 'login_created'),
    url(r'^user/disconnected/', user.disconnected, name = 'disconnected'),

    url(r'^help/', user.help, name = 'help'),
#)
]

SOCIAL_AUTH_URL_NAMESPACE = 'social'
