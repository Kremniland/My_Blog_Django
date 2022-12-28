from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='media', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    publisher = models.BooleanField(default=True)

    category = models.ManyToManyField('Category', related_name='post')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    message = models.CharField(max_length=5000)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Comments(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments_post',
        verbose_name='Комментарии'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Автор комментария'
    )
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата написания')
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(default=False, verbose_name='Видимость комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
