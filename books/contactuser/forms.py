from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import ContactUser


class ContactUserForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = ContactUser
        fields = ('email', 'captcha')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        }
        labels = {
            'email': ''
        }
