from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .viewsets import RecordViewsets


router = DefaultRouter()

router.register(r"record", RecordViewsets, basename="record")


urlpatterns = router.urls