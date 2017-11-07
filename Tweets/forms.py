from django import forms
from django.core.validators import RegexValidator

from .models import Profile


validate_alphanumeric = RegexValidator(r"^\w*$", 'Only alphanumeric characters and underscore are allowed.')


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(validators=[validate_alphanumeric])

    class Meta:
        model = Profile
        fields = ["nickname", "about"]
        widgets = {
            "nickname": forms.TextInput(attrs={"class": "form-control"}),
            "about": forms.Textarea(attrs={"class": "form-control"}),
        }
