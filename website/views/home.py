from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from cron.models import Photo
from cron.models import Album
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
import urllib
from PIL import Image
from social.apps.django_app.default.models import UserSocialAuth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import ftplib
import os
import time
from django.core.exceptions import ObjectDoesNotExist

def index(request):

    context = RequestContext(request,
                                 {'user': request.user})

    if not request.user.is_authenticated():

        return render_to_response('home/index.html',
                                      context_instance=context)
    else:

        return HttpResponseRedirect("/home/")


@login_required
def start(request):


    try:
        album = Album.objects.get(album_name='album_' + settings.TWITTER_SEARCHED_HASHTAG)
        all_photos = Photo.objects.filter(photo_album=album).order_by('-photo_likes')
        paginator = Paginator(all_photos, 10)
        page = request.GET.get('page')
        photos = paginator.page(page)

    except ObjectDoesNotExist as e:
        return render(request, 'home/home.html', {'photos': [], 'message':'Album are not created yet, application must work with an Album'})
    except PageNotAnInteger:

        photos = paginator.page(1)
    except EmptyPage:

        photos = paginator.page(paginator.num_pages)

    return render(request,'home/home.html',{'photos': photos})


@login_required
def post(request):

    if not request.is_ajax():
        return HttpResponse(status=401)
    try:
        album = Album.objects.get(album_name='album_'+settings.TWITTER_SEARCHED_HASHTAG)
    except  ObjectDoesNotExist as e:

        return JsonResponse({
            'response':'KO'
        })

    photos = Photo.objects.filter(photo_album=album).order_by('-photo_likes')[0:7]

    images = []
    for photo in photos:

        if photo.photo_url != '':

            urllib.urlretrieve(photo.photo_url, 'website'+settings.STATIC_URL+'image/'+str(photo.photo_post_id)+".jpg")
            images.append('website'+settings.STATIC_URL+'image/'+str(photo.photo_post_id)+".jpg")

    try:

        images = map(Image.open, images)
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        #new_im.resize((400, 300), Image.NEAREST)#.thumbnail((400,300),Image.ANTIALIAS)
        name = str(time.time()) + ".jpg"
        new_im.save('website'+settings.STATIC_URL + "image/" + name)

        session = ftplib.FTP(settings.HOST_FTP, settings.HOST_FTP_USER, settings.HOST_FTP_PASS)
        file = open('website'+settings.STATIC_URL+"image/"+name, 'rb')
        session.storbinary('STOR '+ name, file)
        file.close()
        session.quit()

        for photo in photos:

            if os.path.exists(os.path.dirname(os.path.dirname(__file__)) + settings.STATIC_URL + 'image/' + str(photo.photo_post_id) + ".jpg"):
                    os.remove(os.path.dirname(os.path.dirname(__file__))+settings.STATIC_URL+'image/'+str(photo.photo_post_id)+".jpg")

        result = {
            'url': settings.HOST_PHOTO_URL + "/"+name,
            'message':'Best photo of %s album!'% (settings.TWITTER_SEARCHED_HASHTAG),
            'title': settings.TWITTER_SEARCHED_HASHTAG,
            'server':'http://stefanocampese.xyz',
            'response':'OK'
        }
    except Exception as e:
        print e
        result = {'response':'KO'}

    return JsonResponse(result)