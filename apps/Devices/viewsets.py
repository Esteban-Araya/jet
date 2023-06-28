from rest_framework import viewsets
from apps.Users.models import Users
from .serializer import DevicesSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

JWT_authenticator = JWTAuthentication()

class DevicesViwests(viewsets.ModelViewSet):
    serializer_class = DevicesSerializer
    queryset = serializer_class.Meta.model.objects.all()
    serializer_token = TokenObtainPairSerializer
    queryset_user = Users.objects.all()

    def partial_update(self, request ,*args, **kwargs):
        """
        Add devices to others users

        you need send the user main token and send the email the other user in the body. Example: {"email" : "person@gmail.com"}
        """
        response = JWT_authenticator.authenticate(request)
        if response is None:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
        user, token = response
        
        email = request.data["email"]
        device = self.get_object()
        
        if not user == device.id_user_main:
            return Response({"message": "tokern no valido"},status=status.HTTP_401_UNAUTHORIZED)
        
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

    def list(self, request, *args, **kwargs):
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
                         "devices": devices.data }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Use this whit token

        
        Use this whit token
        
        """

        response = JWT_authenticator.authenticate(request)
        if response is None:
            return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
        user, token = response
        id_user = token.payload['user_id']
        data = request.data
        data["id_user_main"] = id_user

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        device = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
          
        return Response(serializer.data, 
          status=status.HTTP_201_CREATED, headers=headers)        

