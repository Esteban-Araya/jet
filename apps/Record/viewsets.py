
from rest_framework import viewsets
from apps.Devices.models import Devices
from .serializer import RecordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.mixins import CreateModelMixin

# Create your views here.

JWT_authenticator = JWTAuthentication()

# Create your views here.
class RecordViewsets(viewsets.GenericViewSet, CreateModelMixin):
    serializer_class = RecordSerializer
    queryset = serializer_class.Meta.model.objects.all()
    queryset_device = Devices.objects.all()

    def list(self, request):
        pass

    def create(self, request, *args, **kwargs):
        device_id =request.data["device_id"]
        response = JWT_authenticator.authenticate(request)

        if response is None:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
        user, token = response
        request.data["user_id"] = user.id
        
        device = self.queryset_device.filter(id = device_id)
        
        if user.my_devices.filter(id = device_id) or user.devices.filter(id = device_id): 
            device = device[0]
            device.state = request.data["state"]
            device.save()

            return super().create(request, *args, **kwargs)
        
        if not device:
            return Response({"message":f"device ({device_id}) does not exist" }, status=status.HTTP_400_BAD_REQUEST) 

        return Response({"message":f"{user.username} does not have access to this device" }, status=status.HTTP_400_BAD_REQUEST) 
    
    
