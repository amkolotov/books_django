from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, Rating, Star


class ReviewForm(forms.ModelForm):
    """Форма добавления отзыва"""
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('username', 'email', 'text', 'captcha')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'id': 'comment'})
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=Star.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)
