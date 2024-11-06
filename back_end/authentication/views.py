from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model

from authentication.serializers import LoginSerializer, SignupSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is None:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({'message': 'User logged in'}, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    def post(self, request):
        if request.user.is_anonymous:
            return Response({'message': 'User is not logged in'}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
    

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
