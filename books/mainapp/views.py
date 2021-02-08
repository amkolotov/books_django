from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Book, Genre, Author, Rating
from .forms import ReviewForm, RatingForm


class Years:
    """Миксин для получения годов выхода книг"""
    @staticmethod
    def get_years():
        return Book.objects.filter(draft=False).values('year').order_by('-year').distinct()


class BooksView(Years, ListView):
    """Вывод полного списка книг"""
    model = Book
    queryset = Book.objects.filter(draft=False)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context['genres'] = Genre.objects.all()
    #     return context

    paginate_by = 2


class BookDetailView(Years, DetailView):
    """Вывод детальной информации о книге"""
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


class AddReviewView(View):
    """Добавление отзыва"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.book = book
            form.save()
        return redirect(book.get_absolute_url())


class AuthorDetailView(Years, DetailView):
    """Вывод информации об авторе"""
    model = Author
    template_name = 'mainapp/author.html'
    slug_field = 'name'


class AuthorsView(Years, ListView):
    """Авторы книг"""
    model = Author
    queryset = Author.objects.order_by('name')


class FilterBooksView(Years, ListView):
    """Фильтрация по жанрам и годам"""
    paginate_by = 1

    def get_queryset(self):
        queryset = Book.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = ''.join([f'year={year}&' for year in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f'genre={genre}&' for genre in self.request.GET.getlist('genre')])
        return context


class AddRatingView(View):
    """Добавление или обновление рейтинга книги"""
    def post(self, request):
        print(request.POST)
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                book_id=int(request.POST.get('book')),
                defaults={'rating_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SearchBooksView(ListView):
    """Поиск книг по названию"""
    paginate_by = 1

    def get_queryset(self):
        return Book.objects.filter(title__icontains=self.request.GET.get('search'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f'search={self.request.GET.get("search")}&'

        return context
