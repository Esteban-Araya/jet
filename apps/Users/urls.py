from rest_framework.routers import DefaultRouter
from .viewsets import UserViewsets

router = DefaultRouter()

router.register(r"user", UserViewsets, basename="user")

urlpatterns = router.urls
