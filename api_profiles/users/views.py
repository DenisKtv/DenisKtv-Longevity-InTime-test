from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile
from rest_framework.exceptions import PermissionDenied
from .utils import get_token_for_user
from .serializers import (UserProfileSerializer, UserLoginSerializer,
                          UserProfileDetailSerializer)


class UserRegistrationView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        access_token = get_token_for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "access_token": access_token
            },
            status=201
        )


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")

        access_token = get_token_for_user(user)

        return Response({
            "message": "User authorized successfully",
            "access_token": access_token,
        }, status=200)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'email'

    def get_object(self):
        email = self.kwargs['email'].lower()
        obj = get_object_or_404(UserProfile, email=email)

        if (self.request.method not in permissions.SAFE_METHODS and
                obj.email != self.request.user.email):
            raise PermissionDenied(
                "You do not have permission to access this profile"
            )

        return obj
