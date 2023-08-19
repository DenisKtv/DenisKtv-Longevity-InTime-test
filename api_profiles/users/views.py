from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .api_docs import (user_registration_responses, user_login_responses,
                       user_delete_responses, user_retrieve_responses,
                       user_update_responses)
from .models import UserProfile
from .serializers import (UserLoginSerializer, UserProfileDetailSerializer,
                          UserProfileSerializer)
from .utils import get_token_for_user


class UserRegistrationView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        operation_description='Register a new user',
        responses=user_registration_responses()
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
            status=status.HTTP_201_CREATED
        )


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        operation_description='Authenticate a user and return an access token',
        responses=user_login_responses()
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        access_token = get_token_for_user(user)
        return Response({
            'message': 'User authorized successfully',
            'access_token': access_token,
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'email'

    @swagger_auto_schema(
        operation_description='Retrieve a user profile by email',
        responses=user_retrieve_responses()
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update a user profile by email',
        responses=user_update_responses()
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Partially update a user profile by email',
        responses=user_update_responses()
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Delete a user profile by email',
        responses=user_delete_responses()
    )
    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {'message': 'User profile deleted successfully'},
                status=status.HTTP_200_OK
            )
        return response

    def get_object(self):
        email = self.kwargs['email'].lower()
        obj = get_object_or_404(UserProfile, email=email)

        if (self.request.method not in permissions.SAFE_METHODS and
                obj.email != self.request.user.email):
            raise PermissionDenied(
                'You do not have permission to access this profile'
            )

        return obj
