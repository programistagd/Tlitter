from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

app_name = 'Tweets'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^profile/<pk>/$', views.profile, name='profile'),
    url(r'^settings/$', views.profile_settings, name='profile_settings'),
    url(r'^me/$', views.myprofile, name='myprofile'),
    url(r'^tweet/$', views.post_tweet, name='post_tweet'),
]
