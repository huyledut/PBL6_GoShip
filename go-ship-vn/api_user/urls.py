from rest_framework import routers
from .views import *

app_name = 'api_user'
router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename="user")
urlpatterns = router.urls