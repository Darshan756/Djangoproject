from django.test import TestCase

# Create your tests here
# blog/tests.py

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
            date_posted=timezone.now(),
        )

    def test_post_creation(self):
        """
        Test creating a Post instance.
        """
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post content.')
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(isinstance(self.post.date_posted, timezone.datetime))

    def test_str_method(self):
        """
        Test the string representation (__str__ method) of Post.
        """
        self.assertEqual(str(self.post), 'Test Post')

    def test_get_absolute_url(self):
        """
        Test the get_absolute_url method of Post.
        """
        # Replace 'post-detail' with your actual URL name for post detail view
        expected_url = '/post/{}/'.format(self.post.pk)
        self.assertEqual(self.post.get_absolute_url(), expected_url)

# blog/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
        )

    def test_home_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-create'), {
            'title': 'New Test Post',
            'content': 'This is new test post content.',
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful creation

    # Add more test methods for other views (ListView, UpdateView, DeleteView, etc.)

    def test_about_view(self):
        response = self.client.get(reverse('blog-about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')
        self.assertContains(response, 'about')

    def test_user_post_list_view(self):
        response = self.client.get(reverse('user-posts', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_posts.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    # Add more tests as needed for other views

# blog/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class TestTemplates(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
        )

    def test_home_template(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        #self.assertContains(response, 'Recent Posts')  # Adjust this to match your actual home.html content

    def test_post_detail_template(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_user_posts_template(self):
        response = self.client.get(reverse('user-posts', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_posts.html')
        self.assertContains(response, self.user.username)  # Check for user's posts listing

    def test_about_template(self):
        response = self.client.get(reverse('blog-about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')
       # self.assertContains(response, 'About Us')  # Adjust to match your about.html content

