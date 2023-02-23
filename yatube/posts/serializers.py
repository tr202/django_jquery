from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Comment, Image, Follow, Gallery, Group, Post, PostType
from users.serializers import UserSerialiser


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class GallerySerialiser(serializers.ModelSerializer):
    gallery_images = ImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = ['gallery_images']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class GroupSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = ['id', 'type']


class CreateTypeGalleryPostSerializer(serializers.ModelSerializer):
    #post_gallerys = GallerySerialiser(source='gallerys', many=True)

    class Meta:
        model = Post
        fields = ('title', 'text', 'group',)


class PostSerializer(serializers.ModelSerializer):

    comments_count = serializers.IntegerField(
        source='comments.count',
        read_only=True,
    )

    pub_date = serializers.DateTimeField(format="%d %m %Y")
    # gallerys = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # post_gallery = GallerySerialiser(source='gallerys',)
    author = UserSerialiser()
    group = GroupSerialiser()
    type = PostTypeSerializer()
    post_gallerys = GallerySerialiser(source='gallerys', many=True)

    class Meta:
        model = Post
        fields = ['id', 'type', 'title', 'text', 'pub_date', 'author', 'group', 'post_gallerys', 'comments_count']


class PostWithCommentsSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(format="%d %m %Y")
    comments = CommentSerializer(many=True)
    author = UserSerialiser()
    group = GroupSerialiser()
    type = PostTypeSerializer()
    post_gallerys = GallerySerialiser(source='gallerys', many=True)

    class Meta:
        model = Post
        fields = ['id', 'type', 'title', 'text', 'pub_date', 'author', 'group', 'post_gallerys', 'comments']


