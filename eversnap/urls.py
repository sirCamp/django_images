import website.views.home
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^$', website.views.home.index, name='index'),
    url(r'^home/$', website.views.home.start, name='start'),
    url(r'^post/$', website.views.home.post, name='post'),
    url(r'^api/v1/', include('api.urls')),
]
