from rest_framework import generics, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, ConfirmShipperSerializer, ShipperSerializer, AddressSerializer, UserSerializer
from api_account.models import Account, Shipper, Address, User
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import  Client
import jwt
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
from .permissions import *
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
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        account = Account.objects.filter(Q(phone_number=phone_number))
        if account.exists():
            account = account.first()
            if check_password(password, account.password):
                token = MyTokenObtainPairSerializer.get_token(account)
                response = {
                    'role': account.role,
                    'phone_number': account.phone_number,
                    'access_token': str(token),
                    "details": "Đăng ký thành công!"
                }
                return Response(response,  status=status.HTTP_202_ACCEPTED)
        return Response(
            {
               "details": "Tài khoản đã tồn tại!"
            }, status=status.HTTP_400_BAD_REQUEST, headers=headers)


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
                "details": "Đăng nhập thành công!"
            }
            return Response(response,  status=status.HTTP_202_ACCEPTED)
    return Response({"details": "Số điện thoại hoặc mật khẩu không hợp lệ!"}, status=status.HTTP_400_BAD_REQUEST)


class Account_OTP(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            phone_number = request.data.get("phone_number")
            otp = request.data.get("otp")
            account_sid = 'AC69e64d1e3a974b090a6b8d4d2b2bc08d'
            auth_token = 'kl'
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
                'status': 'Số điện thoại không hợp lệ!',
                'except': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ConfirmShipper(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        phone_number = request.data.get('phone_number')
        address = Address.objects.create(**request.data.get('address'))
        address.save()
        account = Account.objects.get(pk= phone_number)
        shipper = Shipper.objects.get(pk=account)
        shipper.gender = request.data.get('gender')
        shipper.name = request.data.get('name')
        shipper.url_identification_top = request.data.get('url_identification_top')
        shipper.url_identification_back = request.data.get('url_identification_back')
        shipper.url_identification_info = request.data.get('url_identification_info')
        shipper.url_face_video = request.data.get('url_face_video')
        shipper.address = address
        shipper.save()
        data = ShipperSerializer(shipper)
        return Response(data = {
            'status': 'Success',
            'shipper':data.data,
            'address': AddressSerializer(address).data,
            "details": "Đăng nhập thành công!"
        },
        status = status.HTTP_200_OK)


class ShipperViewSet(APIView):
    permission_classes = [ShipperPermission]
    def get(self, request):
        payload = jwt.decode(jwt=request.headers.get('Token'), key=settings.SECRET_KEY, algorithms=['HS256'])
        account = Account.objects.get(pk = payload['phone_number'])
        shipper= Shipper.objects.get(pk =account)    
        serializer = ShipperSerializer(shipper)
        return Response(data={
            'shipper': serializer.data,
            'address': AddressSerializer(shipper.address).data
        }, status=status.HTTP_200_OK)

class UserViewSet(APIView):
    permission_classes = [UserPermission]
    def get(self, request):
        payload = jwt.decode(jwt=request.headers.get('Token'), key=settings.SECRET_KEY, algorithms=['HS256'])
        account = Account.objects.get(pk = payload['phone_number'])
        user= User.objects.get(pk =account)    
        serializer = UserSerializer(user)
        return Response(data={
            'user': serializer.data,
            'address': AddressSerializer(user.address).data
        }, status=status.HTTP_200_OK)

class CheckAccount(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone_number = request.data['phone_number'] 
        account = Account.objects.filter(pk=phone_number)
        if account.exists():
            return Response(data={
               'status': 'Số điện thoại đã được sử dụng!',
            }, status=status.HTTP_200_OK)
        return Response(data={
               'status': 'Số điện thoại chưa sử dụng!',
            }, status=status.HTTP_200_OK)