from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UserProfile
from users.serializers import UserLoginSerializer, UserProfileDetailSerializer


class UserRegistrationViewTest(APITestCase):

    def test_registration_with_existing_email(self):
        existing_user_data = {
            'email': 'test@example.com',
            'password': 'ValidPassword123',
        }
        UserProfile.objects.create_user(**existing_user_data)
        url = reverse('register')
        response = self.client.post(url, existing_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'user profile with this email already exists.', str(response.data))

    def test_registration_with_invalid_data(self):
        url = reverse('register')
        invalid_data = {
            'email': 'test@example.com',
            'password': 'short',
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'Password must be at least 9 characters long', str(response.data)
        )


class TestUserLoginView:
    @pytest.mark.django_db
    def test_user_login_invalid_credentials(self):
        client = APIClient()
        data = {
            'email': 'invalid@example.com',
            'password': 'InvalidPassword',
        }
        response = client.post('/login/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data


@pytest.mark.django_db
class TestUserLoginSerializer:

    def test_invalid_email(self):
        data = {
            'email': 'invalid@example.com',
            'password': 'Password123',
            'otp': '123456',
        }

        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_invalid_password(self):
        user = get_user_model()
        user.objects.create_user(
            email='test@example.com',
            password='Password123',
            is_active=True,
        )
        data = {
            'email': 'test@example.com',
            'password': 'InvalidPassword',
            'otp': '123456',
        }

        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    @patch('users.serializers.send_otp_email.delay')
    @patch('users.serializers.UserProfile.objects.get')
    def test_missing_otp(self, mocked_get_user, mocked_send_otp):
        user = get_user_model()
        mocked_get_user.return_value = user(
            email='test@example.com', password='Password123', is_active=True
        )
        mocked_send_otp.return_value = None

        data = {
            'email': 'test@example.com',
            'password': 'Password123',
        }
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()

        non_field_errors = serializer.errors.get('non_field_errors', [])
        error_messages = [str(error) for error in non_field_errors]
        assert 'Invalid login credentials' in error_messages


@pytest.fixture
def user_with_token():
    user = UserProfile.objects.create_user(
        email='test@example.com',
        password='Password123',
        is_active=True
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return user, access_token


@pytest.mark.django_db
class TestUserProfileView:
    def test_retrieve_user_profile(self, user_with_token):
        user, token = user_with_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = client.get(reverse('profile', kwargs={'email': user.email}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == UserProfileDetailSerializer(user).data

    def test_update_user_profile(self, user_with_token):
        user, token = user_with_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        new_email = 'newname@new.com'
        data = {
            'first_name': 'newname',
            'last_name': 'newname',
            'email': new_email
        }

        response = client.put(
            reverse('profile', kwargs={'email': user.email}), data
        )
        assert response.status_code == status.HTTP_200_OK

        updated_user = UserProfile.objects.get(email=new_email)
        assert updated_user.first_name == 'newname'
        assert updated_user.last_name == 'newname'
        assert updated_user.email == new_email

    def test_partial_update_user_profile(self, user_with_token):
        user, token = user_with_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        new_first_name = "Newname"
        data = {
            'first_name': new_first_name
        }

        response = client.patch(
            reverse('profile', kwargs={'email': user.email}), data
        )
        assert response.status_code == status.HTTP_200_OK

        updated_user = UserProfile.objects.get(email=user.email)
        assert updated_user.first_name == new_first_name

    def test_delete_user_profile(self, user_with_token):
        user, token = user_with_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = client.delete(
            reverse('profile', kwargs={'email': user.email})
        )
        assert response.status_code == status.HTTP_200_OK

        assert not UserProfile.objects.filter(email=user.email).exists()

    def test_update_another_user_profile(self, user_with_token):
        user, token = user_with_token
        another_user = UserProfile.objects.create_user(
            email='another@example.com',
            password='Password123',
            is_active=True
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        data = {'first_name': 'newname'}
        response = client.put(
            reverse('profile', kwargs={'email': another_user.email}), data
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_another_user_profile(self, user_with_token):
        user, token = user_with_token
        another_user = UserProfile.objects.create_user(
            email='another@example.com',
            password='Password123',
            is_active=True
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = client.delete(
            reverse('profile', kwargs={'email': another_user.email})
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert UserProfile.objects.filter(email=another_user.email).exists()
