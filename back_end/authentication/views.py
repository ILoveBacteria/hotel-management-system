from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from authentication.serializers import LoginSerializer, SignupSerializer, MessageSerializer


@extend_schema_view(
    post=extend_schema(
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
)
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            errors = {'message': 'Serializer validation error', **serializer.errors}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is None:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({'message': 'User logged in'}, status=status.HTTP_200_OK)
    

@extend_schema_view(
    post=extend_schema(
        summary="User Logout",
        description="Endpoint for user logout",
        responses={
            200: "Logout successful",
            400: "User is not logged in",
        },
    )
)
class LogoutView(APIView):
    def post(self, request):
        if request.user.is_anonymous:
            return Response({'message': 'User is not logged in'}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
    

@extend_schema_view(
    post=extend_schema(
        summary="User Signup",
        description="Endpoint for user registration",
        request=SignupSerializer,
        responses={201: SignupSerializer},
    )
)
class RegisterView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'message': 'User is already logged in'}, status=status.HTTP_400_BAD_REQUEST)
        super().post(request, *args, **kwargs)
        login(request, self.user)
        return Response({'message': 'User signed up and logged in'}, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        self.user = serializer.save()
