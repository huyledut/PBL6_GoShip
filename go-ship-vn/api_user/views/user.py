from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from api_user import serializers
from api_user.models import User
from api_user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True): 
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

# class ResgisterAPIView(viewsets.ModelViewSet, generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         instance = serializer.save()
#         instance.set_password(instance.password)
#         instance.save()

# class LoginAPIView(viewsets.ModelViewSet, generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     @action(detail=True, methods=['post'])
#     def get_user(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
    # def post(self, request):
    #     user  = User.objects.get(phone_number=request.data['phone_number']).first()
    #     if not user:
    #         raise APIException("invalid credentials")
    #     if not user.check_password(request.data['password']):
    #         raise APIException("invalid credentials")
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)