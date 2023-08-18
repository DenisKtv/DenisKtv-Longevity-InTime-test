from django.contrib import admin
from django.urls import path
from users.views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    path('admin/', admin.site.urls),
]
