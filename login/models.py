from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    sign_date = models.DateTimeField()
    refresh_token = models.CharField(max_length=256)