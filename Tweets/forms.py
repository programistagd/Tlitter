from django import forms

class TweetForm(forms.Form):
    text = forms.CharField()
