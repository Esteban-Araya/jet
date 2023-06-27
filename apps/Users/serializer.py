from rest_framework import serializers
from .models import Users
from apps.Devices.serializer import DevicesSerializer
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        
        exclude = ['is_staff','is_active','last_login',]
    
    def create(self, validated_data):
        user = Users(**validated_data)
        print(user)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data["password"])
        return user
    
    def to_representation(self, instance):
        devices = DevicesSerializer(instance.devices.all(), many = True)
        my_devices = DevicesSerializer(instance.my_devices.all(), many = True)

        
        return {
                "id": instance.id,
                "username": instance.username,
                "email": instance.email,
                "phoneNumber": instance.phoneNumber,
                "profilePicture": instance.profilePicture,
                "devices":devices.data,
                "my_devices":my_devices.data
                }


class UserLoginSerializer(serializers.Serializer):
    
    password = serializers.CharField(max_length=20, )
    email = serializers.EmailField()
    # id = serializers.UUIDField()

    def validate(self, data):
        
        try:
            usuario = Users.objects.filter(email=data["email"])[0]
            
            if not check_password(data["password"], usuario.password):
                raise serializers.ValidationError("Email y/o contraseña incorrectos")
        except:  
            raise serializers.ValidationError("Email o contraseña incorrectos")

        return data
