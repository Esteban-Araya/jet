from django.shortcuts import render
from rest_framework import viewsets
from .models import Users
from .serializer import UserRegistrerSerializer, UserLoginSerializer
from json import loads
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserRegistrerView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserRegistrerSerializer
    permission_classes = (IsAuthenticated,)

    


class LoginView(TokenObtainPairView):

    serializer_class = TokenObtainPairSerializer
    
    def post(self, request):
        print(request.data)
        user = UserLoginSerializer(data=request.data)
        if not user.is_valid():
            print(user.errors)
            return Response({'error': user.errors}, status=status.HTTP_401_UNAUTHORIZED)
        
       
        
        login = self.serializer_class(data = request.data)

        if login.is_valid():
        
            return Response({'token': login.validated_data.get('access')}, status=status.HTTP_200_OK)     
        
        return Response({'error': login.errors}, status=status.HTTP_401_UNAUTHORIZED)
             
        