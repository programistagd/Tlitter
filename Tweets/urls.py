from django.conf.urls import url

from . import views

app_name = 'Tweets'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all/$', views.index_all, name='all'),
    url(r'^following/$', views.following, name='following'),
    url(r'^profile/(?P<name>\w+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<name>\w+)/follow/$', views.follow, name='follow'),
    url(r'^profile/(?P<name>\w+)/unfollow/$', views.unfollow, name='unfollow'),
    url(r'^settings/$', views.profile_settings, name='profile_settings'),
    url(r'^me/$', views.myprofile, name='myprofile'),
    url(r'^tweet/$', views.post_tweet, name='post_tweet'),
]
