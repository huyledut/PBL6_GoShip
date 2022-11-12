from rest_framework import serializers
from .models import Account, User, Shipper, Address, User
import time

from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        account.password = make_password(validated_data['password'])
        account.save()
        text_time = round(time.time()*1000)
        if validated_data['role'] == 1:
            name_default = 'User' + str(text_time)[:10]
            user = User.objects.create(user_id=account, name=name_default)
            user.save()
            print('Tao user')
        elif validated_data['role'] == 2:
            name_default = 'Shipper' + str(text_time)[:10]
            shipper = Shipper.objects.create(
                shipper_id=account, name=name_default)
            shipper.save()
            print('Tao shipper')
        return account


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ConfirmShipperSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)

    class Meta:
        model = Shipper
        fields = ['gender', 'address', 'name', 'url_identification_top',
                  'url_identification_back', 'identification_info', 'url_face_video']


class ShipperSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)

    class Meta:
        model = Shipper
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone_number', 'password']
