from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from blog.models import Post, Comment
from blog.serializers import PostSerializer, CommentSerializer
import json


class PostTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.post1 = Post.objects.create(title='Test Post 1', text='Test text 1')
        self.post2 = Post.objects.create(title='Test Post 2', text='Test text 2')
        self.comment1 = Comment.objects.create(post=self.post1, text='Test comment 1')
        self.comment2 = Comment.objects.create(post=self.post1, text='Test comment 2')
        self.comment3 = Comment.objects.create(post=self.post2, text='Test comment 3')

    def test_post_list_api(self):
        """Проверка работы метода list - просмотра списка постов"""
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        posts = json.loads(response.content)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['title'], 'Test Post 2')
        self.assertEqual(posts[0]['last_comment_text'], 'Test comment 3')
        self.assertEqual(posts[1]['title'], 'Test Post 1')
        self.assertEqual(posts[1]['last_comment_text'], 'Test comment 2')

    def test_post_retrieve_api(self):
        """Проверка метода GET для получения информации по конкретному посту"""
        response = self.client.get(reverse('post-detail', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        post = json.loads(response.content)
        self.assertEqual(post['title'], 'Test Post 1')

    def test_post_view(self):
        """Проверка работы счётчика просмотров"""
        response = self.client.get(reverse('post-detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post 1')
        self.assertContains(response, 'Test text 1')
        self.post1.refresh_from_db()
        post_views = self.post1.views
        response = self.client.get(reverse('post-detail', args=[self.post1.id]))
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.views, post_views + 1)
