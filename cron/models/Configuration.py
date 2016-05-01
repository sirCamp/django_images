from django.db import models

class Configuration(models.Model):
    configuration_key = models.CharField(max_length=500)
    configuration_value = models.CharField(max_length=500)