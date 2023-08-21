from django.contrib.auth.hashers import check_password
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
            {'message': 'OTP sent to your email.'}
        )

    if not check_otp(email, otp):
        raise serializers.ValidationError('Invalid OTP')

    return data


def validate_name(value):
    if value and not value.isalpha():
        raise serializers.ValidationError(
            'Name must contain only letters.'
        )
    return value


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}
    )
    otp = serializers.CharField(required=False, write_only=True)
    first_name = serializers.CharField(
        validators=[validate_name], required=False
    )
    last_name = serializers.CharField(
        validators=[validate_name], required=False
    )

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
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one digit.'
            )
        return value

    def validate(self, data):
        email = data.get('email').lower()
        if UserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Email already exists in our database'
            )
        return validate_otp_data(data)

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
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
        email = data.get('email').lower()

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError(
                'Email does not exist in our database'
            )

        password = data.get('password')
        is_password_valid = check_password(password, user.password)
        is_user_active = user.is_active
        if not is_password_valid or not is_user_active:
            raise serializers.ValidationError('Invalid login credentials')

        validate_otp_data(data)
        return {'user': user}


class UserProfileDetailSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    last_login = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    first_name = serializers.CharField(
        validators=[validate_name], required=False
    )
    last_name = serializers.CharField(
        validators=[validate_name], required=False
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
