from django.shortcuts import render
from rest_framework import viewsets
from .models import Users
from .serializer import UserSerializer, UserLoginSerializer
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
    # print(queryset)
    # print(Users.objects.all())
    #queryset = Users

   
    def create(self, request, *args, **kwargs):
        """
        Use this

        
        Use this
        
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        """
        Use this

        
        Con solo poner el token que te da el 'Login' basta
        
        """
        response = JWT_authenticator.authenticate(request)
        if response is not None:
           # unpacking
           user , token = response
           
           
           user = self.queryset.objects.filter(email=user)
           user = self.serializer_class(user,many = True)
           
           return Response({"User":user.data})
        

        
        return Response({"error": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )

    # def put(self, request, *args, **kwargs):
    #     response = JWT_authenticator.authenticate(request)
    #     if response is not None:
    #        # unpacking
    #        user , token = response
           
    #        return user.put(request, *args, **kwargs)
        

        
    #     return Response({"error": "token no valido"},status=status.HTTP_401_UNAUTHORIZED)
        
   



    

    
    

class LoginView(viewsets.ModelViewSet):

    """
    NO use this

        
    NO use this
    
    """

    serializer_class = UserLoginSerializer
    serializer_token = TokenObtainPairSerializer
    queryset = Users
    def list(self, request):

        """
        Use this

        
        Use this
        
        """

        user = self.serializer_class(data=request.data)
        if not user.is_valid():

            return Response({'errors': user.errors}, status=status.HTTP_401_UNAUTHORIZED)
        
       
        
        login = self.serializer_token(data = request.data)

        if login.is_valid():
        
            return Response({'token': login.validated_data.get('access'),"refresh":login.validated_data.get('refresh')}, status=status.HTTP_200_OK)     
        
        return Response({'error': login.errors}, status=status.HTTP_401_UNAUTHORIZED)
             
        