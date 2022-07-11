from curses import A_PROTECT
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post, Category
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class PostTests(APITestCase):
    def test_view_posts(self):
        """
        Ensure we can view all objects.
        """

        url = reverse('blog_api:list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_unauthenticated(self):
        """
        Ensure we can't create a new Post object if user is not authenticated.
        """
        test_category = Category.objects.create(name='django')
        test_user1 = User.objects.create_user(
            username='test_user1', password='123456789')

        data = {'title': 'Post Title', 'author': 1,
                'excerpt': 'Post Excerpt', 'content': 'Post Content'}

        url = reverse('blog_api:list_create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post(self):
        """
        Ensure we can create a new Post object and view object. 
        """
        client = APIClient()

        self.test_category = Category.objects.create(name='django')
        self.test_user1 = User.objects.create_user(
            username='test_user1', password='123456789')

        data = {'title': 'Post Title', 'author': 1,
                'excerpt': 'Post Excerpt', 'content': 'Post Content'}

        client.login(username=self.test_user1.username,
                     password='123456789')

        url = reverse('blog_api:list_create')
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_update(self):
        """
        Ensure that only author can modify 
        """
        client = APIClient()

        self.test_category = Category.objects.create(name='django')
        self.test_user1 = User.objects.create_user(
            username='test_user1', password='123456789')
        self.test_user2 = User.objects.create_user(
            username='test_user2', password='123456789')
        test_post = Post.objects.create(
            category_id=1, title='Post Title', excerpt='Post Excerpt', content='Post Content', slug='post-title', author_id=1, status='published')

        client.login(username=self.test_user2.username,
                     password='123456789')

        url = reverse(('blog_api:details_create'), kwargs={'pk': 1})

        response = client.put(
            url, {
                "title": "New",
                "author": 1,
                "excerpt": "New",
                "content": "New",
                "status": "published"
            }, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
