
from django.db import models
from cron.models.Album import Album
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Photo(models.Model):

    photo_url = models.CharField(max_length=500)
    photo_https_url = models.CharField(max_length=500)
    photo_hashtags = models.CharField(max_length=500)
    photo_user = models.CharField(max_length=500)
    photo_user_name = models.CharField(max_length=500)
    photo_likes = models.IntegerField()
    photo_post_id = models.BigIntegerField()
    photo_hash = models.CharField(max_length=1024)
    photo_created_at = models.DateTimeField()
    photo_album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return "Id: "+str(self.id) + " Name: "+str(self.photo_post_id)+" URL: "+self.photo_url+" User: "+self.photo_user+" Album: "+self.photo_album.album_name
