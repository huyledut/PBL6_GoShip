from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer
from api_account.models import Account
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import phonenumbers
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, account):
        token = super().get_token(account)
        token['role'] = account.role
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    password = request.data.get("password")
    phone_number = request.data.get("phone_number")
    account = Account.objects.filter(Q(phone_number=phone_number))
    if account.exists():
        account = account.first()
        if check_password(password, account.password):
            token = MyTokenObtainPairSerializer.get_token(account)
            response = {
                'role': account.role,
                'phone_number': account.phone_number,
                'access_token': str(token),
            }
            return Response(response)

    return Response({"details": "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)


