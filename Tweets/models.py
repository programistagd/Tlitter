from django.db import models
from django.utils import timezone
from django.conf import settings

class Profile(models.Model):
    nickname = models.CharField(max_length=32, unique=True)
    about = models.CharField(max_length=140)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.nickname


class Tweet(models.Model):
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField('post date', default=timezone.now)

    def __str__(self):
        return self.text
