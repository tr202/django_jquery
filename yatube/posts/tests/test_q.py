from django.test import TestCase, Client

from http import HTTPStatus

from ..models import Group, Post

from django.urls import reverse

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import connection
from django.conf.urls import url
from . . import views


User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Группа',
            slug='slug',
            description='Описание группы',
        )

        cls.author = User.objects.create(
            username='Автор'
        )
        cls.another_user = User.objects.create_user(
            username='Не авторизованный пользователь'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Пост',
            group=cls.group,
        )
        cls.post1 = Post.objects.create(
            author=cls.author,
            text='Пост',
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
       
    def test(self):
        try:
            print(reverse('posts:post_create'), 'first')
           
        except Exception as e:
            print(e.args)
        #self.assertContains(response, '<img')
        #exists_post_count = Post.objects.count()
        #print(exists_post_count, 'Before') 
        #connection.cursor().execute('DELETE FROM  posts_post')
        #print(Post.objects.count(), 'After')
       
'''       
        self.authorized_client.post(
            reverse('posts:post_create'),
            data={'text': 'Проверка'},
            follow=True,)
        self.assertTrue(Post.objects.count() > exists_post_count)
        latest_post = Post.objects.latest('pub_date')
        self.assertEqual(latest_post.text, 'Проверка')
        self.assertEqual(latest_post.author, self.author)
        
           
    def qtest_cr(self):
        response = self.authorized_client_author.get(f'/posts/{self.post.pk}/edit/')
        print(response.status_code)
        self.assertTemplateUsed(response, 'posts/create_post.html')
'''        