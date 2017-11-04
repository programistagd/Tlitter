from django.template.defaulttags import register


@register.inclusion_tag("Tweets/tweet.html")
def show_tweet(tweet):
    return {"tweet": tweet}
