from unicodedata import name
from django.urls import path
from rest_framework import routers
from .views import RegisterViewSet
from api_account.views import login_view,Account_OTP
from django.views.decorators.csrf import csrf_exempt
name_app = 'register'
router = routers.SimpleRouter()
router.register(r'register', RegisterViewSet, basename='register')
urlpatterns = [
    path("login/", csrf_exempt(login_view), name="login"),
    path("send-otp/",Account_OTP.as_view(), name="send-otp"),
]
urlpatterns += router.urls
