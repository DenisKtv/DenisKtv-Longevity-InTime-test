from drf_yasg import openapi

from .serializers import UserProfileSerializer


def user_registration_responses():
    return {
        201: UserProfileSerializer(),
        400: openapi.Response(description='Validation Error', examples={
            'application/json': {
                'message': 'Validation Error',
                'details': [
                    'Email is required.',
                    'Email must be unique.',
                    'Password must be at least 9 characters long.',
                    'Password must contain at least one uppercase letter.',
                    'First name must contain only letters.',
                    'Last name must contain only letters.',
                    'Invalid OTP',
                ]
            }
        }),
    }


def user_login_responses():
    return {
        200: openapi.Response(
            description='User authorized successfully',
            examples={
                'application/json': {
                    'message': 'User authorized successfully',
                    'access_token': 'example-access-token',
                }
            }),
        400: openapi.Response(description='Validation Error', examples={
            'application/json': {
                'message': 'Validation Error',
                'details': [
                    'Invalid login credentials',
                    'Invalid OTP',
                    'OTP sent to your email.',
                ]
            }
        }),
    }


def user_retrieve_responses():
    return {
        200: openapi.Response(description='Successful retrieval', examples={
            'application/json': {
                "id": 0,
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "date_joined": "2019-08-24T14:15:22Z",
                "last_login": "2019-08-24T14:15:22Z"
            }
        }),
        403: openapi.Response(description='Permission Denied'),
        404: openapi.Response(description='Not Found'),
    }


def user_update_responses():
    return {
        200: openapi.Response(description='Successful update', examples={
            'application/json': {
                "id": 0,
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "date_joined": "2019-08-24T14:15:22Z",
                "last_login": "2019-08-24T14:15:22Z"
            }
        }),
        400: openapi.Response(description='Validation Error'),
        403: openapi.Response(description='Permission Denied'),
        404: openapi.Response(description='Not Found'),
    }


def user_delete_responses():
    return {
        200: openapi.Response(description='Successful deletion', examples={
            'application/json': {
                'message': 'User profile deleted successfully'
            }
        }),
        403: openapi.Response(description='Permission Denied'),
        404: openapi.Response(description='Not Found'),
    }
