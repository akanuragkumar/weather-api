from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .redis import redis_instance
from user.services import UserService
user_service = UserService()


class UserRegisterView(APIView):
    '''user registration- email and password'''
    permission_classes = [AllowAny]

    def post(self, request):
        return user_service.register(data=request.data)


class UserLoginView(APIView):
    '''user login- email and password'''
    permission_classes = [AllowAny]

    def post(self, request):
        return user_service.login(data=request.data)
