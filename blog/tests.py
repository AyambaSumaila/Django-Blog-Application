from django.test import TestCase, Client
from django.urls import reverse 
from django.contrib.auth import get_user_model


# Create your tests here.
from .models import Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='secret')
        

        self.post = Post.objects.create(
            title='A sample title',
            body='A sample body',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)


    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A sample title')
        self.assertEqual(f'{self.post.body}', 'A sample body')
        self.assertEqual(f'{self.post.author}', 'testuser')


    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A sample title')
        self.assertTemplateUsed(response, 'home.html')


    def test_post_detail_view(self):
        response=self.client.get('/post/1/')
        no_response=self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A sample title')
        self.assertTemplateUsed(response, 'post_detail.html')

        