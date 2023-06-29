from rest_framework.routers import DefaultRouter
from .viewsets import LoginView,UserRegisterView


router = DefaultRouter()


router.register(r"login", LoginView, basename="login")
router.register(r"register", UserRegisterView, basename="register")


urlpatterns = router.urls
    