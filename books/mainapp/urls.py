from django.urls import path

from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.BooksView.as_view(), name='index'),

    path('author/', views.AuthorsView.as_view(), name='authors'),
    path('author/<str:slug>/', views.AuthorDetailView.as_view(), name='author'),

    path('review/<int:pk>/', views.AddReviewView.as_view(), name='add_review'),

    path('filter/', views.FilterBooksView.as_view(), name='filter'),
    path('search/', views.SearchBooksView.as_view(), name='search'),

    path('add_rating/', views.AddRatingView.as_view(), name='add_rating'),

    path('<str:slug>/', views.BookDetailView.as_view(), name='detail'),
]