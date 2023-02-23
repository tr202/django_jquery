from django.conf import settings
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from sorl.thumbnail.admin import AdminImageMixin

from .models import Comment, Gallery, Image, Follow, Group, Post, PostType

VERBOSE_NAME_FOR_GET_POST_AUTHOR_NAME = 'Автор поста'
VERBOSE_NAME_FOR_GET_POST_TEXT = 'Начало статьи'


def get_post_gallerys(post):
    return post.gallerys.all()





@admin.register(PostType)
class PostTypeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'type',
    )

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'gallery',
        'image',
    )

    def get_images(self, image):
        return (f'{image.gallery}')
    get_images.__name__ = 'Галлерея'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'get_post_text',
        'get_images',
    )

    def get_post_text(self, gallery):
        return gallery.post.text[:30]
    get_post_text.__name__ = 'Начало статьи'

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'author',
                    'follow_at',
                    )
    search_fields = ('user', 'author')
    list_filter = ('follow_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'created',
                    'author',
                    'text',
                    'get_post_text',
                    'get_post_author_name',
                    )
    list_editable = ('text',)
    search_fields = ('text', 'created', 'post', )
    list_filter = ('created',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }

    def get_post_author_name(self, comment):
        return (f'{comment.post.author.first_name}'
                f'{comment.post.author.last_name}')
    get_post_author_name.__name__ = 'Автор статьи'

    def get_post_text(self, comment):
        return comment.post.text[:200]
    get_post_text.__name__ = 'Начало статьи'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title',
                    'text',
                    'pub_date',
                    'author',
                    'group',
                    'type',
                    'get_post_images'
                    )
    list_editable = ('title', 'group', 'type')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

    def get_post_images(self, post):
        return get_post_gallerys(post)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
