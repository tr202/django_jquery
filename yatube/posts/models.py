from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint

from .utils import slugify
from .validators import not_empty_text_validator as netv


User = get_user_model()


class Group(models.Model):
    title = models.CharField('Заголовок', max_length=200,)
    slug = models.SlugField(
        'Slug-группы',
        unique=True,
        blank=False,
        help_text=('Укажите адрес для страницы задачи. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )
    description = models.TextField('Описание',)

    class Meta:
        verbose_name_plural = 'Сообщества'
        verbose_name = 'сообщество'
        ordering = ('title',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


#  types_items = (
# 'quote', 'video',
#  standard: standard_entry, gallery: gallery_entry, audio: audio_entry}
types_items = [
    ('quote_entry', 'quote'), ('video_entry', 'video'),
    ('standard_entry', 'standard'), ('gallery_entry', 'gallery'),
    ('audio_entry', 'audio')]


class PostType(models.Model):
    type = models.CharField('type', max_length=30,)

    def __str__(self):
        return str(self.type)


class Post(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField(
        'Текст статьи', validators=[netv],
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Сообщество',
    )

    type = models.ForeignKey(
        PostType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Тип поста',
    )

    class Meta:
        verbose_name = 'cтатью'
        verbose_name_plural = 'Статьи'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Gallery(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='gallerys',
        verbose_name='Статья',
    )

    def get_images(self):
        return self.images.all()

    def __str__(self):
        return self.post.__str__()


class Image(models.Model):
    gallery = models.ForeignKey(
        Gallery,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Картинки',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )

    text = models.TextField(
        'Текст комментария',
        validators=[netv],
    )

    created = models.DateTimeField('Дата публикации', auto_now_add=True,)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    follow_at = models.DateTimeField('Дата публикации', auto_now_add=True,)

    class Meta:
        constraints = (
            CheckConstraint(
                name='no_follow_author',
                check=~Q(user=F('author')),
            ),
            UniqueConstraint(
                name='no_double_follow',
                fields=['user', 'author']
            ),
        )
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-follow_at',)

    def __str__(self):
        return self.user.username + ' подписан на ' + self.author.username
