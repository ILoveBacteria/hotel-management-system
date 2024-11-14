from drf_spectacular.utils import extend_schema, OpenApiExample

from authentication.serializers import LoginSerializer, SignupSerializer, MessageSerializer
from authentication import message


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
                value={'message': message.INVALID_USERNAME_OR_PASSWORD},
                status_codes=[400],
                response_only=True,
            ),
            OpenApiExample(
                name='User logged in',
                description='User successfully logged in',
                value={'message': message.USER_LOGGED_IN},
                status_codes=[200],
                response_only=True,
            ),
            OpenApiExample(
                name='Serializer error',
                description='Serializer validation error',
                value={
                    'username': ['This field may not be blank.'], 
                    'password': ['This field may not be blank.']
                    },
                status_codes=[400],
                response_only=True,
            ),
        ],
    )
}

logout_documentation = {
    'post': extend_schema(
        summary="User Logout",
        description="Endpoint for user logout",
        responses={200: MessageSerializer, 400: MessageSerializer},
        examples=[
            OpenApiExample(
                name='User is not logged in',
                description='User is not logged in',
                value={'message': message.USER_NOT_LOGGED_IN},
                status_codes=[400],
                response_only=True,
            ),
            OpenApiExample(
                name='User logged out',
                description='User successfully logged out',
                value={'message': message.USER_LOGGED_OUT},
                status_codes=[200],
                response_only=True,
            ),
        ],
    )
}

register_documentation = {
    'post': extend_schema(
        summary="User Signup",
        description="Endpoint for user registration",
        request=SignupSerializer,
        responses={201: MessageSerializer, 400: MessageSerializer},
        examples=[
            OpenApiExample(
                name='User is already logged in',
                description='User is already logged in',
                value={'message': message.USER_ALREADY_LOGGED_IN},
                status_codes=[400],
                response_only=True,
            ),
            OpenApiExample(
                name='User signed up and logged in',
                description='User successfully signed up and logged in',
                value={'message': message.USER_SIGNED_UP_AND_LOGGED_IN},
                status_codes=[201],
                response_only=True,
            ),
            OpenApiExample(
                name='Serializer error',
                description='Serializer validation error',
                value={
                    'first_name': ['This field may not be blank.'], 
                    'last_name': ['This field may not be blank.'],
                    'username': [
                        'This field may not be blank.', 
                        'A user with that username already exists.'
                        ],
                    'email': [
                        'This field may not be blank.', 
                        'Enter a valid email address.'
                        ],
                    'password': ['This field may not be blank.']
                    },
                status_codes=[400],
                response_only=True,
            ),
        ],
    )
}