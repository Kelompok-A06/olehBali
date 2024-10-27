from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .forms import PostForm, CommentForm
import json

class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content'
        )

    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.__str__(), 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test Content')

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test Comment'
        )

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(self.comment.__str__(), f"Comment by {self.user} on {self.post}")
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, 'Test Comment')

class PostFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'title': 'Test Post',
            'content': 'Test Content'
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'title': '',  # Title is required
            'content': 'Test Content'
        }
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())

class CommentFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'content': 'Test Comment'
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'content': ''  # Content is required
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test Content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test Comment'
        )

    def test_post_list_view(self):
        # Test unauthenticated access
        response = self.client.get(reverse('community:post_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test authenticated access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('community:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/post_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('community:post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/post_detail.html')

    def test_create_post(self):
        # Test unauthenticated access
        response = self.client.post(reverse('community:create_post'), {
            'title': 'New Post',
            'content': 'New Content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test authenticated access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:create_post'), {
            'title': 'New Post',
            'content': 'New Content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to post_list
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_ajax_create_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('community:create_post'),
            {'title': 'Ajax Post', 'content': 'Ajax Content'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])

    def test_delete_post(self):
        # Test unauthenticated access
        response = self.client.post(reverse('community:delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test authenticated but unauthorized access
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('community:delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

        # Test authorized access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_create_comment(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('community:create_comment', args=[self.post.id]),
            {'content': 'New Comment'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(Comment.objects.filter(content='New Comment').exists())

    def test_delete_comment(self):
        # Test unauthorized access
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('community:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

        # Test authorized access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_json_endpoints(self):
        # Test show_json
        response = self.client.get(reverse('community:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Test show_json_by_id
        response = self.client.get(reverse('community:show_json_by_id', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Test show_comments_json
        response = self.client.get(reverse('community:show_comments_json', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_xml_endpoints(self):
        # Test show_xml
        response = self.client.get(reverse('community:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        # Test show_xml_by_id
        response = self.client.get(reverse('community:show_xml_by_id', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        # Test show_comments_xml
        response = self.client.get(reverse('community:show_comments_xml', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_update_post(self):
        # Test unauthenticated access
        response = self.client.post(reverse('community:update_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test authenticated but unauthorized access
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('community:update_post', args=[self.post.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        self.assertEqual(response.status_code, 404)

        # Test authorized access
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:update_post', args=[self.post.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        self.assertEqual(response.status_code, 200)
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.content, 'Updated Content')