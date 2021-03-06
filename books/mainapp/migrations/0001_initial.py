# Generated by Django 3.1.5 on 2021-01-21 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Автор')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('death', models.DateField(blank=True, null=True, verbose_name='Дата смерти')),
                ('desc', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='authors/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Книга')),
                ('tagline', models.CharField(default='', max_length=256, verbose_name='Слоган')),
                ('desc', models.TextField(verbose_name='Описание')),
                ('num_of_pages', models.PositiveSmallIntegerField(default=0, verbose_name='Количество страниц')),
                ('cover', models.ImageField(upload_to='covers/', verbose_name='Обложка')),
                ('year', models.PositiveSmallIntegerField(default=2020, verbose_name='Год')),
                ('slug', models.SlugField(max_length=256, unique=True)),
                ('draft', models.BooleanField(default=True, verbose_name='Черновик')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.author', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Жанр')),
                ('desc', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, verbose_name='Издательство')),
            ],
            options={
                'verbose_name': 'Издательство',
                'verbose_name_plural': 'Издательства',
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда',
                'verbose_name_plural': 'Звезды',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='Имя пользователя')),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.book', verbose_name='Книга')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.reviews', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP адрес')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.book', verbose_name='Книга')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.star', verbose_name='Рэйтинг')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='book_images/', verbose_name='Изображение книги')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.book', verbose_name='Книга')),
            ],
            options={
                'verbose_name': 'Изображение книги',
                'verbose_name_plural': 'Изображения книг',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(to='mainapp.Genre', verbose_name='Жанр'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.publisher', verbose_name='Издательство'),
        ),
        migrations.AddField(
            model_name='book',
            name='tag',
            field=models.ManyToManyField(to='mainapp.Tag', verbose_name='Teг'),
        ),
    ]
