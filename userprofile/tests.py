# userprofile/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            role='user'  
        )
        self.profile = Profile.objects.create(
            user=self.user,
            name='Test User',
            phone_number='1234567890',
            email='testuser@example.com',
            birthdate='1990-01-01'
        )

    def test_dashboard_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('userprofile:dashboard', args=[self.user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, 'My Account')
        self.assertContains(response, self.profile.name)

    def test_update_profile_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('userprofile:update_profile', args=[self.user.id]), {
            'name': 'Updated Name',
            'phone_number': '0987654321',
            'email': 'updated@example.com',
            'birthdate': '1990-01-01',
            'avatar': ''  
        })
        
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'message': 'Profile updated successfully',
            'data': {
                'name': 'Updated Name',
                'phone_number': '0987654321',
                'email': 'updated@example.com',
                'birthdate': '1990-01-01',
                'avatar_url': None
            }
        })
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, 'Updated Name')
        self.assertEqual(self.profile.phone_number, '0987654321')
        self.assertEqual(self.profile.email, 'updated@example.com')

    def test_profile_creation(self):
        """Test that a Profile is created with valid fields."""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.name, 'Test User')
        self.assertEqual(self.profile.phone_number, '123456789')
        self.assertEqual(self.profile.email, 'test@example.com')
        self.assertEqual(str(self.profile.birthdate), '1990-01-01')

    def test_profile_str_method(self):
        """Test the string representation of the Profile."""
        self.assertEqual(str(self.profile), 'Test User')
        
    def test_profile_user_relationship(self):
        """Test that the profile is linked to the correct user."""
        self.assertEqual(self.profile.user.email, self.user.email)

    def test_profile_fields_are_not_null(self):
        """Test that Profile fields cannot be null."""
        with self.assertRaises(Exception):
            Profile.objects.create(
                user=self.user,
                name=None,
                phone_number=None,
                email=None,
                birthdate=None
            )

    def test_delete_account_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.delete(reverse('userprofile:delete_account'), 
                                       data='{"confirm": true}', 
                                       content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'redirect_url': reverse('authentication:login_register')
        })
        
        # Check if the user is deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')


    def tearDown(self):
        # Clean up after tests
        self.user.delete()
        self.profile.delete()
