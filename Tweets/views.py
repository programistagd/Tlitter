from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Tweet, Profile
from .forms import ProfileForm


def index(request):
    if request.user.is_authenticated:
        return redirect("Tweets:following")
    return redirect("Tweets:all")


def index_all(request):
    tweets = Tweet.objects.order_by('-pub_date')[:10]
    ctx = {"latest_tweets": tweets,
           "head_text": "Most recent tweets"}
    return render(request, "Tweets/index.html", ctx)


@login_required
def following(request):
    try:
        prof = request.user.profile
    except ObjectDoesNotExist:
        return redirect("Tweets:profile_settings")
    followed_profiles = prof.following.values_list("target", flat=True)
    tweets = Tweet.objects.filter(poster__in=followed_profiles)
    ctx = {"latest_tweets": tweets,
           "head_text": "Tweets by people you follow"}
    return render(request, "Tweets/index.html", ctx)


def _handle_profile(request, profile):
    tweets = profile.tweet_set.order_by("-pub_date")[:10]
    ctx = {"profile": profile, "tweets": tweets}
    return render(request, "Tweets/profile.html", ctx)


def _go_back(request):
    if "next" in request.GET:
        return redirect(request.GET["next"])
    return redirect("/")


def profile(request, name):
    try:
        prof = Profile.objects.filter(nickname=name)[0]
        return _handle_profile(request, prof)
    except IndexError:
        return render(request, "Tweets/not_found.html",
                      {"text": "User not found"}, status=404)


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
            mock_prof = Profile(user=request.user)
        form = ProfileForm(request.POST, instance=mock_prof)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect("Tweets:myprofile")
    else:
        try:
            form = ProfileForm(instance=request.user.profile)
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
