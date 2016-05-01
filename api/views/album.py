from cron.models import Album
from django.http import JsonResponse
from django.core import serializers

def get_albums(request,first,limit):

    response = {}
    response['albums'] = serializers.serialize('json',Album.objects.order_by('id')[first:limit])
    return JsonResponse(response)

def get_album_by_id(request,album_id):

    response = {}
    response['albums'] = serializers.serialize('json',Album.objects.filter(pk=album_id))
    return JsonResponse(response)
