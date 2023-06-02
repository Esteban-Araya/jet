from django.shortcuts import render
from rest_framework import viewsets
from .models import Users
from .serializer import UserRegistrerSerializer, UserLoginSerializer
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

class UserRegistrerView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserRegistrerSerializer

    # def put(self, request, *args, **kwargs):
    #     response = JWT_authenticator.authenticate(request)
    #     if response is not None:
    #        # unpacking
    #        user , token = response
           
    #        return user.put(request, *args, **kwargs)
        

        
    #     return Response({"error": "token no valido"},status=status.HTTP_401_UNAUTHORIZED)
        
   

class UserGetView(APIView):
    queryset = Users.objects.all()
    serializer_class = UserRegistrerSerializer

    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        response = JWT_authenticator.authenticate(request)
        if response is not None:
           # unpacking
           user , token = response
           
           
           user = Users.objects.filter(email=user)
           user = UserRegistrerSerializer(user,many = True)
           
           return Response({"User":user.data})
               
        return Response({"error": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )

    

class LoginView(TokenObtainPairView):

    serializer_class = TokenObtainPairSerializer
    
    def post(self, request):

        user = UserLoginSerializer(data=request.data)
        if not user.is_valid():

            return Response({'error': user.errors}, status=status.HTTP_401_UNAUTHORIZED)
        
       
        
        login = self.serializer_class(data = request.data)

        if login.is_valid():
        
            return Response({'token': login.validated_data.get('access'),"refresh":login.validated_data.get('refresh')}, status=status.HTTP_200_OK)     
        
        return Response({'error': login.errors}, status=status.HTTP_401_UNAUTHORIZED)
             
        