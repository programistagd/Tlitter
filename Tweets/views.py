from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Tweet, Profile, Following
from .forms import ProfileForm


def index(request):
    if request.user.is_authenticated:
        return redirect("Tweets:following")
    return redirect("Tweets:all")


TWEETS_ON_PAGE = 10


def index_all(request):
    tweets = Tweet.objects.order_by('-pub_date')[:TWEETS_ON_PAGE]
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
    tweets = Tweet.objects.filter(poster__in=followed_profiles).order_by("-pub_date")[:TWEETS_ON_PAGE]
    ctx = {"latest_tweets": tweets,
           "head_text": "Tweets by people you follow"}
    return render(request, "Tweets/index.html", ctx)


def _following_query(follower, target):
    return Following.objects.filter(follower=follower, target=target)


def _handle_profile(request, profile):
    following = None
    try:
        if request.user.is_authenticated and request.user.profile != profile:
            following = _following_query(request.user.profile, profile).count() > 0
    except ObjectDoesNotExist:
        pass

    # Here I assume that the amount of followers is quite small and display all of them
    followed_profiles = profile.following.values_list("target__nickname", flat=True)
    following_profiles = profile.followers.values_list("follower__nickname", flat=True)
    tweet_query = profile.tweet_set.order_by("-pub_date")
    pages = int(tweet_query.count() / TWEETS_ON_PAGE) + 1
    page = 0
    if "page" in request.GET:
        page = int(request.GET["page"]) - 1

    tweets = profile.tweet_set.order_by("-pub_date")[TWEETS_ON_PAGE * page:TWEETS_ON_PAGE * page + TWEETS_ON_PAGE]

    ctx = {"profile": profile,
           "tweets": tweets,
           "followed_profiles": followed_profiles,
           "following_profiles": following_profiles,
           "following": following,
           "pages": pages,
           "page": page + 1,
           "pagesRange": range(1, pages + 1)} # TODO maybe show not all?
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


def profile_operation(operation):
    @login_required
    def view(request, name):
        if request.method != "POST":
            return HttpResponseForbidden("Wrong method")
        try:
            target = Profile.objects.filter(nickname=name)[0]
            follower = request.user.profile
            operation(follower, target)
            return redirect("Tweets:profile", name)
        except IndexError:
            return render(request, "Tweets/not_found.html",
                          {"text": "User not found"}, status=404)
        except ObjectDoesNotExist:
            return redirect("Tweets:profile_settings")
    return view


@profile_operation
def follow(follower, target):
    if _following_query(follower, target).count() > 0:
        return #already following

    relation = Following(follower=follower, target=target)
    relation.save()


@profile_operation
def unfollow(follower, target):
    _following_query(follower, target).delete()
