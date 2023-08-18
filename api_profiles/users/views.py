from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import (UserLoginSerializer, UserProfileDetailSerializer,
                          UserProfileSerializer)
from .utils import get_token_for_user


class UserRegistrationView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        operation_description='Register a new user',
        responses={
            201: UserProfileSerializer()},
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        access_token = get_token_for_user(user)

        return Response(
            {
                'message': 'User registered successfully',
                'access_token': access_token
            },
            status=201
        )


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        operation_description='Authenticate a user and return an access token',
        responses={200: UserLoginSerializer()},
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')

        access_token = get_token_for_user(user)

        return Response({
            'message': 'User authorized successfully',
            'access_token': access_token,
        }, status=200)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'email'

    @swagger_auto_schema(
            operation_description='Retrieve a user profile by email'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_description='Update a user profile by email'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_description='Delete a user profile by email'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        email = self.kwargs['email'].lower()
        obj = get_object_or_404(UserProfile, email=email)

        if (self.request.method not in permissions.SAFE_METHODS and
                obj.email != self.request.user.email):
            raise PermissionDenied(
                'You do not have permission to access this profile'
            )

        return obj
