from django.http import HttpResponse
from django.core.mail import get_connection, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from cron.models import Photo
from cron.models import Album
from social.apps.django_app.default.models import UserSocialAuth
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from open_facebook import OpenFacebook
from django.http import HttpResponseRedirect, HttpResponse
import urllib

def index(request):

    context = RequestContext(request,
                                 {'user': request.user})
    return render_to_response('home/index.html',
                                  context_instance=context)


@login_required
def start(request):


    facebook = OpenFacebook(UserSocialAuth.objects.get(provider='facebook').tokens)


    print(facebook.get('me'))
    album = get_object_or_404(Album,album_name='album_'+settings.TWITTER_SEARCHED_HASHTAG)
    photos = Photo.objects.filter(photo_album=album)
    return render(request,'home/home.html',{'photos':photos})

def post(request):

    photos = Photo.objects.order_by('-photo_likes')[0:7]

    for photo in photos:
        print photo.photo_post_id
        if photo.photo_url != '':
            urllib.urlretrieve(photo.photo_url, settings.MEDIA_URL+str(photo.photo_post_id)+".jpg")
    import Image
    new_im = Image.new('RGB', (400, 400))
    for photo in photos:


        # opens an image:
        im = Image.open(settings.MEDIA_URL+str(photo.photo_post_id)+".jpg")
        # creates a new empty image, RGB mode, and size 400 by 400.


        # Here I resize my opened image, so it is no bigger than 100,100
        im.thumbnail((100, 100))
        # Iterate through a 4 by 4 grid with 100 spacing, to place my image
        for i in xrange(0, 500, 100):
            for j in xrange(0, 500, 100):
                # I change brightness of the images, just to emphasise they are unique copies.
                #im = Image.eval(im, lambda x: x + (i + j) / 30)
                # paste the image at location i,j:
                new_im.paste(im, (i, j))

        new_im.show()
    return HttpResponse("Hello, world. You're at the polls index.")