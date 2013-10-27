from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web_site.views.lobby'),
    url(r'^lobby/', 'web_site.views.lobby'),
    url(r'^create_pair/', 'web_site.views.create_pair', name='create_pair'),
    url(r'^pair/(\d+)/', 'web_site.views.pair')

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)