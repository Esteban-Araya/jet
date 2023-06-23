from rest_framework.routers import DefaultRouter
from .viewsets import LoginView,UserRegistrerView


router = DefaultRouter()


router.register(r"login", LoginView, basename="device")
router.register(r"registrer", UserRegistrerView, basename="registrer")

# urlpatterns = router.urls

urlpatterns = router.urls
    