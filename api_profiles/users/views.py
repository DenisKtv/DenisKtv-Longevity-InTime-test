from rest_framework import generics
from rest_framework.response import Response
from .models import UserProfile
from .utils import get_token_for_user
from .serializers import UserProfileSerializer, UserLoginSerializer


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
