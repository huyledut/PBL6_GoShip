from unicodedata import name
from django.urls import path
from rest_framework import routers
from .views import RegisterViewSet, ConfirmShipper, ShipperViewSet, UserViewSet,CheckAccount, LoginView
from api_account.views import Account_OTP
from django.views.decorators.csrf import csrf_exempt
name_app = 'register'
router = routers.DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path("login/",LoginView.as_view() , name="login"),
    path("send-otp/",Account_OTP.as_view(), name="send-otp"),
    path("confirm-shipper/", ConfirmShipper.as_view(), name="confirm"),
    path("user/", UserViewSet.as_view(), name="info-user"),
    path("shipper/",ShipperViewSet.as_view(), name="info-shipper"),
    path('check-account/', CheckAccount.as_view(), name="check-account"),
]
urlpatterns += router.urls
