from rest_framework import serializers
from .models import Users, Devices
from django.contrib.auth.hashers import make_password,check_password


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        
        exclude = ['is_staff','is_active','last_login',]
    
    def create(self, validated_data):
        user = Users(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data["password"])
        return user
    # def validate_password(self, value: str) -> str:
    #     """
    #     Hash value passed by user.

    #     :param value: password of a user
    #     :return: a hashed version of the password
    #     """
    #     return make_password(value)

    # def to_representation(self, instance):
        
    #     return instance
          
    


class UserLoginSerializer(serializers.Serializer):
    
    password = serializers.CharField(max_length=20, )
    email = serializers.EmailField()
    # id = serializers.UUIDField()

    def validate(self, data):
        print("---------------------")
        try:
            usuario = Users.objects.filter(email=data["email"])[0]
            
            if not check_password(data["password"], usuario.password):
                raise serializers.ValidationError("Email y/o contraseña incorrectos")
        except:  
            raise serializers.ValidationError("Email o contraseña incorrectos")

        return data
    

class DevicesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Devices