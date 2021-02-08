from django.db import models
from django.urls import reverse


class Genre(models.Model):
    """Жанры книг"""
    name = models.CharField('Жанр', max_length=128)
    desc = models.TextField('Описание')
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    """Авторы книг"""
    name = models.CharField('Автор', max_length=128)
    birthday = models.DateField('Дата рождения')
    death = models.DateField('Дата смерти', blank=True, null=True)
    desc = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='authors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Tag(models.Model):
    """Теги"""
    name = models.CharField('Тег', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Publisher(models.Model):
    """Издательство"""
    name = models.CharField('Издательство', max_length=128, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'


class Book(models.Model):
    """Книги"""
    title = models.CharField('Книга', max_length=256)
    tagline = models.CharField('Слоган', max_length=256, default='')
    tag = models.ManyToManyField(Tag, verbose_name='Teг')
    desc = models.TextField('Описание')
    num_of_pages = models.PositiveSmallIntegerField('Количество страниц', default=0)
    cover = models.ImageField('Обложка', upload_to='covers/')
    year = models.PositiveSmallIntegerField('Год', default=2020)
    publisher = models.ForeignKey(Publisher, verbose_name='Издательство', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(Genre, verbose_name='Жанр')
    slug = models.SlugField(max_length=256, unique=True)
    draft = models.BooleanField('Черновик', default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mainapp:detail', kwargs={'slug': self.slug})

    def get_parent_reviews(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Images(models.Model):
    """"Изображения"""
    image = models.ImageField('Изображение книги', upload_to='book_images/')
    book = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.CASCADE)

    def __str__(self):
        return f'Изображение из книги {self.book.title}'

    class Meta:
        verbose_name = 'Изображение книги'
        verbose_name_plural = 'Изображения книг'


class Star(models.Model):
    """Звезда рейтинга"""
    value = models.IntegerField('Значение', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Звезда'
        verbose_name_plural = 'Звезды'
        ordering = ['-value']


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField('IP адрес', max_length=15)
    rating = models.ForeignKey(Star, verbose_name='Рeйтинг', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book} - {self.rating}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    """Отзывы"""
    username = models.CharField('Имя пользователя', max_length=128)
    email = models.EmailField()
    text = models.TextField()
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username} - {self.book}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
