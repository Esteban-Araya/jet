from rest_framework import viewsets
from .models import Users
from .serializer import UserSerializer, UserLoginSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin


JWT_authenticator = JWTAuthentication()

class UserViewsets(viewsets.GenericViewSet, CreateModelMixin):


    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model
    serializer_token = TokenObtainPairSerializer

    

   
    def create(self, request, *args, **kwargs):
        """
        Register

        
        Request parameters below
        
        \nResponse\n
        {
            'id':'random UUID'
            'token': 'example token'
        }           
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
        Get information about an user

        
        you need put a token        
        """
        
        response = JWT_authenticator.authenticate(request)
        if response is not None:
           # unpacking
           user , token = response
           
           
           user = self.queryset.objects.filter(email=user)[0]
           
           user = self.serializer_class(user,many = False)
          
           return Response(user.data)
        

        
        return Response({"message": "token no valido"},status=status.HTTP_401_UNAUTHORIZED )
    
    @action(detail=False, methods=['post'])
    def login(self, request):

        """
        login user

        
        \nUse this parameters in the request's body\n
        {
            'email': 'email@example.com', 
            'password':'1234ab' 
        }

        \nResponse\n
        {
            'id':'random UUID'
            'token': 'example token'
        }
        """

        user = UserLoginSerializer(data=request.data)

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

  