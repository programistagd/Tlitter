from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory, Textarea
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic

from .models import *
from .forms import TweetForm


class IndexView(generic.ListView):
    template_name = 'Tweets/index.html'
    context_object_name = 'latest_tweets'

    def get_queryset(self):
        """Return the last 10 published tweets."""
        return Tweet.objects.order_by('-pub_date')[:10]


def _handle_profile(request, profile):
    tweets = profile.tweet_set.order_by("-pub_date")[:10]
    return render(request, "Tweets/profile.html", {"profile": profile, "tweets": tweets})


def _go_back(request):
    if "next" in request.GET:
        return redirect(request.GET["next"])
    return redirect("/")


def profile(request, pid):
    prof = get_object_or_404(Profile, pk=pid)
    return _handle_profile(request, prof)


ProfileForm = modelform_factory(Profile, fields=("nickname", "about"), widgets={"about": Textarea()})


@login_required
def myprofile(request):
    try:
        prof = request.user.profile
    except ObjectDoesNotExist:
        return redirect("Tweets:profile_settings")
    return _handle_profile(request, prof)


@login_required
def profile_settings(request):
    if request.method == "POST":
        try:
            mock_prof = request.user.profile
        except ObjectDoesNotExist:
            mock_prof = Profile(user = request.user)
        form = ProfileForm(request.POST, instance = mock_prof)
        # check whether it's valid:
        if form.is_valid():
            prof = form.save()
            return redirect("Tweets:myprofile")
    else:
        try:
            form = ProfileForm(instance = request.user.profile)
        except ObjectDoesNotExist:
            form = ProfileForm()

    return render(request, "Tweets/profile_settings.html", {'form': form})


def post_tweet(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return HttpResponseForbidden("error")

    try:
        text = request.POST["text"]
        prof = request.user.profile
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseForbidden("error")

    if 1 <= len(text) <= 140:
        tweet = Tweet(text=text, poster=prof)
        tweet.save()
        return HttpResponse("OK")
    else:
        return HttpResponseForbidden("error")

