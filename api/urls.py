from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^photo/(?P<album_id>[0-9]+)/from/(?P<first>[0-9]+)/to/(?P<limit>[0-9]+)$', views.get_photos, name='api.get_photos'),
    url(r'^photo/(?P<album_id>[0-9]+)/photo/(?P<photo_id>[0-9]+)$', views.get_photo, name='api.get_photo'),

    url(r'^album/from/(?P<first>[0-9]+)/to/(?P<limit>[0-9]+)$', views.get_albums, name='api.get_albums'),
    url(r'^album/(?P<album_id>[0-9]+)$', views.get_album_by_id, name='api.get_album_by_id'),
]