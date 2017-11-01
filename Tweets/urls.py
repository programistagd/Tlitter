from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

app_name = 'Tweets'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/<pk>/$', views.profile, name='profile'),
    url(r'^settings/$', views.profile_settings, name='profile_settings'),
    url(r'^me/$', views.myprofile, name='myprofile'),
]
