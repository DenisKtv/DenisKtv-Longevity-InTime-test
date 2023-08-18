from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import UserProfile
from .tasks import send_otp_email
from .utils import check_otp


def validate_otp_data(data):
    email = data.get('email')
    otp = data.get('otp')

    if not otp:
        send_otp_email.delay(email)
        raise serializers.ValidationError(
            {"message": "OTP sent to your email."}
        )

    if not check_otp(email, otp):
        raise serializers.ValidationError("Invalid OTP")

    return data


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}
    )
    otp = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'date_joined',
            'last_login',
            'otp'
        ]

    def validate_password(self, value):
        if len(value) < 9:
            raise serializers.ValidationError(
                'Password must be at least 9 characters long.'
            )
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one uppercase letter.'
            )
        return value

    def validate_first_name(self, value):
        if value and not value.isalpha():
            raise serializers.ValidationError(
                'First name must contain only letters.'
            )
        return value

    def validate_last_name(self, value):
        if value and not value.isalpha():
            raise serializers.ValidationError(
                'Last name must contain only letters.'
            )
        return value

    def validate(self, data):
        return validate_otp_data(data)

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=True
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}
    )
    otp = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        validate_otp_data(data)
        email = data.get('email').lower()
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError('Invalid login credentials')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    last_login = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'last_login'
        ]
