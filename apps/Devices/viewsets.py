from rest_framework import viewsets
from .serializer import DevicesSerializer


class DevicesViwests(viewsets.ModelViewSet):
    serializer_class = DevicesSerializer

    queryset = serializer_class.Meta.model.objects.all()




