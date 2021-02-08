from django.shortcuts import render
from django.views.generic import CreateView

from .forms import ContactUserForm
from .models import ContactUser


class ContactUserView(CreateView):
    model = ContactUser
    form_class = ContactUserForm
    success_url = '/'
