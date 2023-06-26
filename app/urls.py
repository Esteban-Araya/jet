from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import  UserRegistrerView, LoginView, DevicesViwests,RecordViewsets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()

router.register(r"user", UserRegistrerView, basename="user")
router.register(r"login", LoginView, basename="user_login")
router.register(r"device", DevicesViwests, basename="device")
router.register(r"record", RecordViewsets, basename="record")


urlpatterns = router.urls
    
