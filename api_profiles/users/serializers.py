from rest_framework import serializers
from .models import UserProfile
from .tasks import send_otp_email
from .utils import check_otp
from django.contrib.auth import authenticate


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
        email = data.get("email").lower()
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return {"user": user}
        raise serializers.ValidationError("Invalid login credentials")


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
