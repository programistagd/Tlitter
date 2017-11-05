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
            "about": forms.Textarea(),
        }
