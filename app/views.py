from django.shortcuts import render
from rest_framework import viewsets
from .models import Users,Devices
from .serializer import UserSerializer, UserLoginSerializer, DevicesSerializer, RecordSerializer
from json import loads
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

JWT_authenticator = JWTAuthentication()

class UserRegistrerView(viewsets.ModelViewSet):

    """
    NO use this

        
    NO use this
    
    """
    
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model
    serializer_token = TokenObtainPairSerializer

    def create(self, request, *args, **kwargs):
        """
        Use this

        }
        Use this
        
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        id = serializer.data["id"]

        login = self.serializer_token(data = request.data)

        if login.is_valid():
        
            return Response({
                        'id':id,
                        "token": login.validated_data.get('access')}, 
                        status=status.HTTP_201_CREATED, headers=headers)        
        
        
        return Response({'message': "info invalida"}, status=status.HTTP_401_UNAUTHORIZED)
        
        

    def list(self, request, *args, **kwargs):
        """
        Use this

        
        Con solo poner el token que te da el 'Login' basta
        
        """
        
        response = JWT_authenticator.authenticate(request)
        if response is not None:
           # unpacking
           user , token = response
           
           
           user = self.queryset.objects.filter(email=user)[0]
           
           user = self.serializer_class(user,many = False)
          
           return Response(user.data)
        

        
        return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )


    
    

class LoginView(viewsets.ModelViewSet):

    """
    NO use this

        
    NO use this
    
            """

    serializer_class = UserLoginSerializer
    serializer_token = TokenObtainPairSerializer
    queryset = Users
    def create(self, request):

        """
        Use this

        
        Use this
        
        """

        
        
        user = self.serializer_class(data=request.data)

        if not user.is_valid():
            
            return Response({'message': "informacion usuario no valida"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = self.queryset.objects.filter(email=user.data["email"])
        
        login = self.serializer_token(data = request.data)

        if login.is_valid():
        
            return Response({
                        'id':user[0].id,
                        "token": login.validated_data.get('access')}
                        , status=status.HTTP_200_OK)     
        
        return Response({'message': "informacion usuario no valida"}, status=status.HTTP_401_UNAUTHORIZED)
             


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
        
class RecordViewsets(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    queryset = serializer_class.Meta.model.objects.all()
    queryset_device = Devices.objects.all()

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
            device.turn_on = request.data["turn_on"]
            device.save()

            return super().create(request, *args, **kwargs)
        
        if not device:
            return Response({"message":f"device ({device_id}) does not exist" }, status=status.HTTP_400_BAD_REQUEST) 

        return Response({"message":f"{user.username} does not have access to this device" }, status=status.HTTP_400_BAD_REQUEST) 
       
    
         
        




