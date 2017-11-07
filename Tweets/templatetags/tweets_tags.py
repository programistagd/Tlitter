from django.template.defaulttags import register
from datetime import timedelta
from django.utils import timezone


@register.inclusion_tag("Tweets/tweet.html")
def show_tweet(tweet):
    return {"tweets": [tweet]}


@register.inclusion_tag("Tweets/tweet.html")
def show_tweets(tweets):
    return {"tweets": tweets}


def _pluralize(amount, prefix, what):
    if amount == 1:
        return prefix + " " + what + " ago"
    return str(amount) + " " + what + "s ago"


@register.filter(name='smartdate')
def smart_date(date):
    elapsed = timezone.now() - date
    if elapsed < timedelta(minutes=1):
        return "a moment ago"
    if elapsed < timedelta(hours=1):
        minutes = int(elapsed.seconds / 60)
        return _pluralize(minutes, "a", "minute")
    if elapsed < timedelta(days=1):
        hours = int(elapsed.seconds / 3600)
        return _pluralize(hours, "an", "hour")
    return date.strftime("%b. %-d, %Y, %H:%M")
