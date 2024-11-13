from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from authentication.serializers import LoginSerializer, SignupSerializer, MessageSerializer


login_documentation = {
    'post': extend_schema(
        summary="User Login",
        description="Endpoint for user login",
        request=LoginSerializer,
        responses={200: MessageSerializer, 400: MessageSerializer},
        examples=[
            OpenApiExample(
                name='Invalid username or password',
                description='User provided invalid username or password',
                value={'message': 'Invalid username or password'},
                status_codes=[400],
                response_only=True,
            ),
            OpenApiExample(
                name='User logged in',
                description='User successfully logged in',
                value={'message': 'User logged in'},
                status_codes=[200],
                response_only=True,
            ),
            OpenApiExample(
                name='Serializer error',
                description='Serializer validation error',
                value={
                    'message': 'Serializer validation error',
                    'username': ['This field may not be blank.'], 
                    'password': ['This field may not be blank.']
                    },
                status_codes=[400],
                response_only=True,
            ),
        ],
    )
}