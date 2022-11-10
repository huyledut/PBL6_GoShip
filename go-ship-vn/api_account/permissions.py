from rest_framework.permissions import BasePermission, SAFE_METHODS
import jwt
from django.conf import settings
from src import settings
class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Token')
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        if payload['role'] == 3:
            return True
        return False

class ShipperPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Token')
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        if payload['role'] == 2:
            return True
        return False

class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Token')
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        if payload['role'] == 1:
            return True
        return False
