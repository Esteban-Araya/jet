from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import  UserRegistrerView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()


router.register(r"user", UserRegistrerView, basename="user")
router.register(r"login", LoginView, basename="user_login")

# urlpatterns = router.urls

urlpatterns = [
    #path('user/', include("router.urls"), name=''),
    #path('user/', UserGetView.as_view()),
    #path('user/registrer/', UserRegistrerView.as_view()),
    #path('user/login/', LoginView.as_view(), name="login"),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + router.urls
    
