from rest_framework.routers import DefaultRouter
from .viewsets import DevicesViwests


router = DefaultRouter()

router.register(r"devices", DevicesViwests, basename="devices")

urlpatterns = router.urls
    