from django.db import models
from django.utils import timezone
from django.conf import settings


class Profile(models.Model):
    nickname = models.CharField(max_length=32, unique=True, db_index=True) #TODO add index here
    about = models.CharField(max_length=140)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, db_index=True)

    def __str__(self):
        return self.nickname


class Tweet(models.Model):
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE, db_index=True) #TODO add index here
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField("post date", default=timezone.now, db_index=True)

    def __str__(self):
        return self.text


class Following(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following")
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return str(self.follower) + " -> " + str(self.target)
