from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import Genre, Author, Tag, Publisher, Book, Images, Star, Rating, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BookAdminForm(forms.ModelForm):
    desc = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Book
        fields = '__all__'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Администрирование жанров"""
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Администрирование авторов"""
    list_display = ('name', 'birthday', 'death', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="auto"')

    get_image.short_description = 'Изображение'

    readonly_fields = ('get_image', )


class ReviewInline(admin.TabularInline):
    """Отображение вложенных отзывов в книге"""
    model = Reviews
    extra = 1
    readonly_fields = ('username', 'email')


class ImagesInline(admin.TabularInline):
    """Отображение вложенных изображений в книге"""
    model = Images
    extra = 1

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="auto"')

    readonly_fields = ('get_image',)
    get_image.short_description = 'Картинка'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Администрирование книг"""
    list_display = ('title', 'year', 'publisher', 'slug', 'draft')
    list_filter = ('year', 'publisher')
    search_fields = ('title', 'genres__name')
    actions = ['publish', 'unpublish']
    inlines = [ImagesInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    form = BookAdminForm
    readonly_fields = ('get_image', )
    # fields = (('title', 'tagline'), ('tag', 'genres'), ('desc',), ('num_of_pages', 'cover'), ('publisher', 'author'),
    #           ('year', 'slug', 'draft'))
    fieldsets = (
        (None, {
            'fields': (('title', 'num_of_pages'),)
        }),
        (None, {
            'fields': (('tagline', 'tag'),)
        }),
        (None, {
            'fields': (('cover', 'get_image'),)
        }),
        (None, {
            'fields': (('author', 'genres'),)
        }),
        ('Описание', {
            'classes': ('collapse',),
            'fields': (('desc',),)
        }),
        (None, {
            'fields': (('publisher', 'year'),)
        }),

        (None, {
            'fields': (('slug', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.cover.url} width="100", height="auto"')

    get_image.short_description = ''

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        set_update = queryset.update(draft=True)
        if set_update == 1:
            message = '1 запись была снята с публикации'
        else:
            message = f'{set_update} записей были сняты с публикации'
        self.message_user(request, message)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    def publish(self, request, queryset):
        """Опубликовать"""
        set_update = queryset.update(draft=False)
        if set_update == 1:
            message = '1 запись опубликована'
        else:
            message = f'{set_update} записей были опубликованы'
        self.message_user(request, message)

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    """Администрирование изображений"""
    list_display = ('book', 'image', 'get_image')
    list_filter = ('book',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50", height="60"')

    get_image.short_description = 'Изображение'
    readonly_fields = ('get_image',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Администрирование отзывов"""
    list_display = ('username', 'email', 'book', 'parent', 'id')
    readonly_fields = ('username', 'email')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating', 'book', 'ip')


# admin.site.register(Genre, GenreAdmin)
# admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Publisher)
# admin.site.register(Book)
# admin.site.register(Images)
admin.site.register(Star)
# admin.site.register(Rating)
# admin.site.register(Reviews)

admin.site.site_title = 'Booker'
admin.site.site_header = 'Booker'
