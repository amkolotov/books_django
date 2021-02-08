from django import template
from django.db.models import Avg

from ..models import Genre, Book, Rating, Star

register = template.Library()


@register.simple_tag
def get_genres():
    return Genre.objects.all()


@register.inclusion_tag('mainapp/tags/last_books.html')
def get_last_books(count=5):
    last_books = Book.objects.order_by('id')[:count]
    return {'last_books': last_books}


@register.simple_tag
def get_rating(pk):
    rating = Rating.objects.filter(book_id=pk).aggregate(avg_rating=Avg('rating__value'))
    if rating['avg_rating']:
        return int(rating['avg_rating'])


@register.simple_tag
def get_star_range():
    return range(Star.objects.all().count())
