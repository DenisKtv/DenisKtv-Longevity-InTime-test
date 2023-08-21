from django.urls import reverse
from rest_framework.test import APITestCase


class URLTests(APITestCase):
    def test_registration_url_resolves(self):
        url = reverse('register')
        self.assertEqual(url, '/register/')

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(url, '/login/')

    def test_profile_url_resolves(self):
        email = 'test@example.com'
        url = reverse('profile', args=[email])
        self.assertEqual(url, f'/profile/{email}/')

    def test_swagger_ui_url_resolves(self):
        url = reverse('schema-swagger-ui')
        self.assertEqual(url, '/swagger/')

    def test_redoc_url_resolves(self):
        url = reverse('schema-redoc')
        self.assertEqual(url, '/redoc/')
