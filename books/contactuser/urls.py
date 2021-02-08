from django.urls import path

from contactuser.views import ContactUserView

app_name = 'contactuser'

urlpatterns = [
    path('', ContactUserView.as_view(), name='index'),
]
