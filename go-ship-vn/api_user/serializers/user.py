from api_user.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    permission_classes = []
    class Meta:
        model = User
        fields = ["phone_number", "password"]
        # extra_kwargs = {
        #     "password": {"write_only": True},
        # }
        def create(self, validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
        
