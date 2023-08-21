from django.test import TestCase
from users.models import UserProfile


class UserProfileModelTestCase(TestCase):
    def test_create_user(self):
        user = UserProfile.objects.create_user(
            email='test@example.com',
            password='Testpass1',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('Testpass1'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = UserProfile.objects.create_superuser(
            email='superuser@example.com',
            password='Superpass1'
        )
        self.assertEqual(user.email, 'superuser@example.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
