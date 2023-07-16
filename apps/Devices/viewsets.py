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
from apps.Invitations.serializer import InvitationSerializer, Invitations
# Create your views here.

JWT_authenticator = JWTAuthentication()

class DevicesViwests(viewsets.GenericViewSet, CreateModelMixin):
    serializer_class = DevicesSerializer
    queryset = serializer_class.Meta.model.objects.all()
    serializer_token = TokenObtainPairSerializer
    queryset_user = Users.objects.all()

    def isNotValidJwt(self, request):
        response = JWT_authenticator.authenticate(request)
        if response is None:
            return True,Response({"message": "token is not valid"},status=status.HTTP_401_UNAUTHORIZED )
        return False, response 

        
    def isOwner(self,user, device):
        if not user == device.id_user_main:
            return Response({"message": "token is not valid"},status=status.HTTP_401_UNAUTHORIZED)
        
        return True

    @action(detail=True, methods=['patch'])
    def reciveInvitation(self, request ,pk=None):
        """
        Accept o reject invitation

        \nIn the {id} put the id of device
        send a token  
        
        \nRequets('true' for accept - 'false' for reject)\n
        {
            "accept":true
        }

        \nResponse\n
        {
            "message": "invitation accepted"
        }
        """
        response = self.isNotValidJwt(request)
        if response[0]:
            return response[1]
        user, token = response[1]
        device = self.get_object()
        invitation = Invitations.objects.filter(reciver=user, device=device)
        if not invitation:
            return Response({"message":"invitation no exist"}, status=status.HTTP_400_BAD_REQUEST)
        # invitation = InvitationSerializer(data={"reciver":user})
        # invitation.is_valid()
        print(invitation[0])
        accept = request.data["accept"]
        if accept:
            device.users_id.add(user)
            invitation[0].delete()
            return Response({"message":"invitation accepted"}, status=status.HTTP_202_ACCEPTED)


        return Response({"message":"invitation rejected"}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def sendInvitation(self, request ,pk=None):
        """
        Send invitations to others users


        In the {id} put the id of device
        send the token of the device's owner 

        \nRequest parameters\n
        {
            'email' : 'person@gmail.com'
        }

        \nResponse\n
        {
            'message':'validation'
        }
        """
        response = self.isNotValidJwt(request)
        if response[0]:
            return response[1]
        user, token = response[1]
        
        device = self.get_object()
        owner = self.isOwner(user, device)
        if not owner:
            return owner
        email = request.data["email"]

        try:
            otherUser = self.queryset_user.filter(email=email)[0]
        except:
            return Response({"message":f"the email {email} does not exist" }, status=status.HTTP_400_BAD_REQUEST) 
        

        if otherUser in device.users_id.all():
            return Response({"message": f"the user {otherUser.username} aleredy had access to {device.name}"},status=status.HTTP_200_OK)
        elif otherUser == user:
                        return Response({"message": f"the user {otherUser.username} aleredy had access to {device.name}"},status=status.HTTP_200_OK)
        data = {
            "reciver": otherUser.id, 
            "owner": user.id, 
            "device": device.id
        }
        invitation = InvitationSerializer(data=data)
        if not invitation.is_valid(raise_exception=True):
             return Response({"message":invitation.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        invitation.save()
        return Response({"message":f"the user {otherUser.username} now has accexs to {device.name}" }, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def history(self, request):
        """
        device's history

        \nsend the token of device's owner
        Request parameters\n
        {
         'id_device': '12345678'
        }

        \nResponse\n
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
        response = self.isNotValidJwt(request)
        if response[0]:
            return response[1]
        user, token = response[1]

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
        


        \nsend the token of devices's owner
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

        response = self.isNotValidJwt(request)
        if response[0]:
            return response[1]
        user, token = response[1]

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

        \nsend the owner's token 
        Request parameters\n
        {
            "id": "12345",
            "name": "porton abajo",
            "device_type": "porton"
        }
        

        \nResponse below
        """

        response = self.isNotValidJwt(request)
        if response[0]:
            return response[1]
        user, token = response[1]
        id_user = token.payload['user_id']
        request.data["id_user_main"] = id_user

        return super().create(request, *args, **kwargs)
    
    