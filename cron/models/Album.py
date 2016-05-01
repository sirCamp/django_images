from django.db import models
from datetime import datetime

class Album(models.Model):
    album_name = models.CharField(max_length=100)
    album_photos = models.CharField(max_length=500)
    album_next_goal = models.IntegerField()
    album_created_at = models.DateTimeField()
    album_updated_at = models.DateTimeField()