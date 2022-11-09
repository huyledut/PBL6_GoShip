from rest_framework import generics, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer
from api_account.models import Account
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import  Client
from rest_framework.views import APIView 
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import phonenumbers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import authentication, permissions
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


class Account_OTP(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            phone_number = request.data.get("phone_number")
            otp = request.data.get("otp")
            account_sid = 'AC69e64d1e3a974b090a6b8d4d2b2bc08d'
            auth_token = 'd42b4486b2488ae41f7823b2819b7c89'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                messaging_service_sid='MG1e5faf909efa83f4c72531147bd4e6d8',
                body='GoShip: Mã xác thực OTP của bạn là ' + otp,
                to=phone_number,
            )
            print(str(message) + "id" +str(message.sid))
            if message.sid:
                print("Send successful")
                return Response(data={
                    'status': 'Success',
                    'phone_number': phone_number,
                }, status=status.HTTP_200_OK)
        
            print("Send failed")
            return Response(data={ 
                'status': 'Failure',
                'phone_number': phone_number,
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={
                'status': 'Phone number is invalid',
                'except': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



