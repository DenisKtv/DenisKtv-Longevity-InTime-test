from unittest.mock import patch

import pytest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import UserProfile
from users.serializers import (UserLoginSerializer,
                               UserProfileDetailSerializer,
                               UserProfileSerializer)


class TestUserRegistration:

    @pytest.mark.django_db
    def test_otp_sent_with_valid_data(self):
        data = {
            'email': 'test@example.com',
            'password': 'Password123',
        }
        with (patch('users.serializers.send_otp_email.delay')
              as mocked_send_otp):
            try:
                UserProfileSerializer().validate(data)
            except ValidationError as e:
                assert str(e.detail['message']) == 'OTP sent to your email.'
                mocked_send_otp.assert_called_once_with(data['email'])

    @pytest.mark.django_db
    def test_user_created_with_valid_data_and_otp(self):
        data = {
            'email': 'test@example.com',
            'password': 'Password123',
            'otp': '123456',
        }

        with patch('users.serializers.check_otp', return_value=True):
            serializer = UserProfileSerializer(data=data)
            assert serializer.is_valid()
            user = serializer.save()

            assert user.email == data['email']

    @pytest.mark.django_db
    def test_registration_with_invalid_otp(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'Password123',
            'otp': 'invalid_otp',
        }

        with patch('users.serializers.check_otp', return_value=False):
            serializer = UserProfileSerializer(data=user_data)
            with pytest.raises(serializers.ValidationError) as e:
                serializer.is_valid(raise_exception=True)

            assert 'Invalid OTP' in str(e.value)

    @pytest.mark.django_db
    def test_registration_with_existing_email(self):
        existing_user_data = {
            'email': 'test@example.com', 'password': 'ValidPassword123'
        }
        UserProfile.objects.create_user(**existing_user_data)

        serializer = UserProfileSerializer(data=existing_user_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'user profile with this email already exists.' in str(e.value)

    @pytest.mark.django_db
    def test_registration_with_no_uppercase_in_password(self):
        user_data = {'email': 'test@example.com', 'password': 'password123'}

        serializer = UserProfileSerializer(data=user_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert ('Password must contain at least one uppercase letter.'
                in str(e.value))

    @pytest.mark.django_db
    def test_registration_with_no_uppercase_in_password(self):
        user_data = {'email': 'test@example.com', 'password': 'password123'}

        serializer = UserProfileSerializer(data=user_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert ('Password must contain at least one uppercase letter.'
                in str(e.value))

    @pytest.mark.django_db
    def test_registration_with_no_digit_in_password(self):
        user_data = {
            'email': 'test@example.com', 'password': 'PasswordWithoutDigit'
        }
        serializer = UserProfileSerializer(data=user_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'Password must contain at least one digit.' in str(e.value)

    @pytest.mark.django_db
    def test_registration_with_short_password(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'Pass123',
        }

        serializer = UserProfileSerializer(data=user_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'Password must be at least 9 characters long.' in str(e.value)


class TestUserLogin:

    @pytest.mark.django_db
    def test_login_with_non_existing_email(self):
        user_data = {
            'email': 'nonexistent@example.com',
            'password': 'Password123',
        }

        serializer = UserLoginSerializer(data=user_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'Email does not exist in our database' in str(e.value)

    @pytest.mark.django_db
    def test_login_with_invalid_password(self):
        existing_user_data = {
            'email': 'test@example.com',
            'password': 'ValidPassword123'
        }
        UserProfile.objects.create_user(**existing_user_data)

        login_data = {
            'email': 'test@example.com',
            'password': 'InvalidPassword123',  # Неправильный пароль
        }

        serializer = UserLoginSerializer(data=login_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'Invalid login credentials' in str(e.value)

    @pytest.mark.django_db
    def test_login_with_inactive_user(self):
        existing_user_data = {
            'email': 'test@example.com',
            'password': 'ValidPassword123'
        }
        user = UserProfile.objects.create_user(**existing_user_data)
        user.is_active = False
        user.save()

        login_data = {
            'email': 'test@example.com',
            'password': 'ValidPassword123',
        }

        serializer = UserLoginSerializer(data=login_data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'Invalid login credentials' in str(e.value)


class TestUserDetail:

    @pytest.mark.django_db
    def test_user_profile_name_validation(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Invalid Name123',
            'last_name': 'Doe'
        }

        serializer = UserProfileDetailSerializer(data=data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'Name must contain only letters.' in str(e.value)

    @pytest.mark.django_db
    def test_user_profile_surname_validation(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Doe',
            'last_name': 'Invalid Surname123'
        }

        serializer = UserProfileDetailSerializer(data=data)
        with pytest.raises(serializers.ValidationError) as e:
            serializer.is_valid(raise_exception=True)

        assert 'Name must contain only letters.' in str(e.value)
