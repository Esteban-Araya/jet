from rest_framework.routers import DefaultRouter
from .viewsets import DevicesViwests


router = DefaultRouter()

router.register(r"device", DevicesViwests, basename="device")

urlpatterns = router.urls
    