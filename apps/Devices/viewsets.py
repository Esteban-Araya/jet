from rest_framework import viewsets
from apps.Users.models import Users
from .serializer import DevicesSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from apps.Record.serializer import RecordSerializer

# Create your views here.

JWT_authenticator = JWTAuthentication()

class DevicesViwests(viewsets.GenericViewSet, CreateModelMixin):
    serializer_class = DevicesSerializer
    queryset = serializer_class.Meta.model.objects.all()
    serializer_token = TokenObtainPairSerializer
    queryset_user = Users.objects.all()

    def isOwner(self,user, device):
        if not user == device.id_user_main:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED)
        
        return True

    def partial_update(self, request ,pk=None):
        """
        Add devices to others users

        In the {id} put the id of device
        send the token of the device's owner 
        Request parameters
        {
            'email' : 'person@gmail.com'
        }

        Response
        {
            'message':'validation'
        }
        """
        response = JWT_authenticator.authenticate(request)
        if response is None:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
        user, token = response
        
        email = request.data["email"]
        device = self.get_object()
        owner = self.isOwner(user, device)
        if not owner:
            return owner
        
        try:
            otherUser = self.queryset_user.filter(email=email)[0]
        except:
            return Response({"message":f"the email {email} does not exist" }, status=status.HTTP_400_BAD_REQUEST) 
        

        if otherUser in device.users_id.all():
            return Response({"message": f"the user {otherUser.username} aleredy had access to {device.name}"},status=status.HTTP_200_OK)
        elif otherUser == user:
                        return Response({"message": f"the user {otherUser.username} aleredy had access to {device.name}"},status=status.HTTP_200_OK)

        device.users_id.add(otherUser)

        return Response({"message":f"the user {otherUser.username} now has accexs to {device.name}" }, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def history(self, request):
        """
        device's history

        send the token of device's owner
        Request parameters
        {
         'id_device': '12345678'
        }

        Response
        {
          'history': [ 
            {
                'time': "2023-06-29T02:23:01.712324Z",
                'state': true,
                'user': 'name user'
            }
          ]
        }
        """
        response = JWT_authenticator.authenticate(request)
        if response is None:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
        user, token = response
        id = request.data["id_device"]
        device = self.queryset.filter(id=id)[0]
        
        owner = self.isOwner(user, device)
        if not owner:
            return owner

        
        device_history =RecordSerializer(device.record.all(), many = True).data
        
        return Response({"history":device_history, 
                          }, status=status.HTTP_200_OK)
        

    def list(self, request, *args, **kwargs):
        """
        get devices
        
        send the token of devices's owner

        Response 
        {
            'my_devices': 
            [
                {
                'id': '241879',
                'name': 'heladera piso bajo',
                'device_type': 'heladera',
                'state': false,
                'id_user_main': '19e43e68-7cf8-4bb7-b238-1092e76dda49',
                'users_id': 
                    [
                    '7c4b3a1a-f081-43a9-b0e8-d3fdb92ba033',
                    'cab8e67d-1f8f-43ee-b0ee-59371e26c1a0'
                    ]
                }
            ],
            'other_devices': [
                {
                'id': '241879',
                'name': 'heladera piso bajo',
                'device_type': 'heladera',
                'state': false,
                'id_user_main': '7c4b3a1a-f081-43a9-b0e8-d3fdb92ba033',         
                'users_id': 
                    [
                    '19e43e68-7cf8-4bb7-b238-1092e76dda49',
                    'cab8e67d-1f8f-43ee-b0ee-59371e26c1a0'
                    ]
                }
            ]
        }
        """

        response = JWT_authenticator.authenticate(request)
        if response is None:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
        user, token = response
        id_user = token.payload['user_id']
        my_devices = self.queryset.filter(id_user_main=id_user)
        my_devices = self.serializer_class(my_devices,many = True)

        devices = self.queryset.filter(users_id=id_user)
        devices = self.serializer_class(devices,many = True)

        return Response({"my_devices":my_devices.data, 
                         "other_devices": devices.data }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        create a devices

        send the owner's token 
        Request parameters
        {
            "id": "12345",
            "name": "porton abajo",
            "device_type": "porton"
        }
        

        Response below
        """

        response = JWT_authenticator.authenticate(request)
        if response is None:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
        user, token = response
        id_user = token.payload['user_id']
        request.data["id_user_main"] = id_user

        return super().create(request, *args, **kwargs)