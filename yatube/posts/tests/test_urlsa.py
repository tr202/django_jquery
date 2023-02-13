from django.test import TestCase, Client

from http import HTTPStatus

from ..models import Group, Post

from django.urls import reverse

from django.contrib.auth import get_user_model

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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client_author = Client()
        self.authorized_client.force_login(self.another_user)
        self.authorized_client_author.force_login(self.author)


    def test_cr(self):
        response = self.authorized_client_author.get(f'/posts/{self.post.pk}/edit/')
        print(response.status_code)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def qtest_url_not_found(self):
        """Запрос к несуществующей странице"""
        response = self.guest_client.get('/page_404/')
        self.assertEqual(response.status_code, 404, HTTPStatus.NOT_FOUND)

    def qtest_correct_url(self):
        """Отклик сайта"""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200, HTTPStatus.OK)


    def qtest_guest_client_url(self):
        """Работа сайта для неавторизованного пользователя"""
        def url(url, **kwargs):
            return reverse(url, kwargs=kwargs)

        test_data = {
            ('posts/index.html', reverse('posts:index'),): HTTPStatus.OK,
            ('posts/group_list.html', url('posts:group_list', slug=self.group.slug),):HTTPStatus.OK,
            ('posts/profile.html', url('posts:profile', username=self.author),):HTTPStatus.OK,
            ('posts/post_detail.html', url('posts:post_detail', post_id=self.post.id),):HTTPStatus.OK,
            (None, url('posts:post_edit', post_id=self.post.id),): HTTPStatus.FOUND,
            (None, url('posts:post_create'),): HTTPStatus.FOUND,
        }
 
        for template_url, status_code in test_data.items():
            r = self.guest_client.get(template_url[1])
            print(template_url[0], template_url[1])
            self. assertEqual(r.status_code, status_code)
            if template_url[0]:
                self.assertTemplateUsed(r, template_url[0])






'''
    def test_authorized_client_url(self):
        """Работа сайта для авторизованного пользователя"""
        def url(url, **kwargs):
            return reverse(url, kwargs=kwargs)

        urls = [
            url('posts:index'),
            url('posts:group_list', slug=self.group.slug),
            url('posts:profile', username=self.author),
            url('posts:post_detail', post_id=self.post.id),
            url('posts:post_edit', post_id=self.post.id),
            url('posts:create_post'),
        ]

        templates = [
            'posts/index.html',
            'posts/group_list.html',
            'posts/profile.html',
            'posts/post_detail.html',
            'posts/create_post.html',
            'posts/create_post.html',
        ]

        for url, template in zip(urls, templates):
            with self.subTest(url=url):
                response = self.authorized_client.get(url).status_code
                self.assertEqual(response, template)

    def test_authorized_client_author_url(self):
        """Работа сайта для авторизованного автора"""
        def url(url, **kwargs):
            return reverse(url, kwargs=kwargs)

        urls = [
            url('posts:index'),
            url('posts:group_list', slug=self.group.slug),
            url('posts:profile', username=self.author),
            url('posts:post_detail', post_id=self.post.id),
            url('posts:post_edit', post_id=self.post.id),
            url('posts:create_post'),
        ]

        templates = [
            'posts/index.html',
            'posts/group_list.html',
            'posts/profile.html',
            'posts/post_detail.html',
            'posts/create_post.html',
            'posts/create_post.html',
        ]

        for url, template in zip(urls, templates):
            with self.subTest(url=url):
                response = self.authorized_client_author.get(url).status_code
                self.assertEqual(response, template)

    def test_template_test(self):
        """Работа шаблонов URL"""
        def url(url, **kwargs):
            return reverse(url, kwargs=kwargs)

        urls = [
            url('posts:index'),
            url('posts:group_list', slug=self.group.slug),
            url('posts:profile', username=self.author),
            url('posts:post_detail', post_id=self.post.id),
            url('posts:post_edit', post_id=self.post.id),
            url('posts:create_post'),
        ]

        templates = [
            'posts/index.html',
            'posts/group_list.html',
            'posts/profile.html',
            'posts/post_detail.html',
            'posts/create_post.html',
            'posts/create_post.html',
        ]

        for url, template in zip(urls, templates):
            with self.subTest(url=url):
                response = self.authorized_client_author.get(url)
                self.assertTemplateUsed(response, template)
'''