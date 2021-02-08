from django.db import models


class ContactUser(models.Model):
    """Подписка на рассылку по email"""
    email = models.EmailField(unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
