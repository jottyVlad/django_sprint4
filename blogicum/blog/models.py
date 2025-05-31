from django.contrib.auth.models import User
from django.db import models


class WithCreatedAtAndPublished(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                                 'чтобы скрыть публикацию.')

    class Meta:
        abstract = True


class Post(WithCreatedAtAndPublished):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время '
                                              'в будущем — можно делать '
                                              'отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор публикации',
                               related_name='posts')
    location = models.ForeignKey('Location',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name='Местоположение',
                                 related_name='posts')
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория',
                                 related_name='posts')
    image = models.ImageField(upload_to='images/',
                              blank=True,
                              verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Публикации'
        verbose_name = 'публикация'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Category(WithCreatedAtAndPublished):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, цифры, '
                                      'дефис и подчёркивание.')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'

    def __str__(self):
        return self.title


class Location(WithCreatedAtAndPublished):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name_plural = 'Местоположения'
        verbose_name = 'местоположение'

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
