from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory, Textarea
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import TweetForm

def index(request):
    return render(request, "Tweets/index.html")

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

@login_required
def tweet(request, text):
    try:
        prof = request.user.profile
    except ObjectDoesNotExist:
        return redirect("Tweets:profile_settings")
    if request.method != "POST":
        return redirect('/')
    form = TweetForm(request.POST)
    if form.is_valid():
        tweet = Tweet(text = form.cleaned_data["text"], poster = prof)
    else:
        return redirect('/')
