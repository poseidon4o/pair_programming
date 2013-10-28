from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url("", include('django_socketio.urls')),
    url(r'^accounts/login/', 'web_site.views.login', name='user_login'),
    url(r'^accounts/logout/', 'web_site.views.logout', name='user_logout'),
    url(r'^accounts/register/', 'web_site.views.register', name='user_register'),
    url(r'^$', 'web_site.views.login'),
    url(r'^lobby/', 'web_site.views.lobby'),
    url(r'^create_pair/', 'web_site.views.create_pair', name='create_pair'),
    url(r'^pair/(\d+)/', 'web_site.views.pair')


    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)