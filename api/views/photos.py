from cron.models import Photo
from cron.models import Album
from django.http import JsonResponse
from django.core import serializers

def get_photos(request,album_id,first,limit):

    response = {}
    response['photos'] = serializers.serialize('json',Photo.objects.filter(photo_album_id=album_id).order_by('id')[first:limit])
    return JsonResponse(response)

def get_photo(request,album_id,photo_id):

    response = {}
    response['photo'] = serializers.serialize('json',Photo.objects.filter(photo_album_id=album_id,pk=photo_id))
    return JsonResponse(response)