from rest_framework import serializers
from .models import Comment, Image, Follow, Gallery, Group, Post, PostType,  User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class GallerySerialiser(serializers.ModelSerializer):
    gallery_images = ImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = ['id', 'post', 'gallery_images']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class GroupSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = ['id', 'type']


class PostSerializer(serializers.ModelSerializer):
   
    comments_count = serializers.IntegerField(
        source='comments.count',
        read_only=True,
    )
    #gallerys_count = serializers.RelatedField(
     #   source='gallerys.count',
      #  read_only=True,
    #)
    gallerys = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # post_gallery = GallerySerialiser(source='gallerys',)
    author = UserSerialiser()
    group = GroupSerialiser()
    type = PostTypeSerializer()
    post_gallerys = GallerySerialiser(source='gallerys', many=True)
   
    #def get_gallery(self, obj):
     #   return obj.gallery

    class Meta:
        model = Post
        fields = ['type', 'title', 'text', 'pub_date', 'author', 'group', 'gallerys', 'post_gallerys', 'comments_count']


class PostWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['text', 'pub_date', 'author', 'group', 'comments']
