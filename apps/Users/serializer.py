from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable
from .models import Users
from apps.Devices.serializer import DevicesSerializer
from apps.Invitations.serializer import InvitationSerializer
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        
        exclude = ['is_staff','is_active','last_login',]
    
    def create(self, validated_data):
        if len(validated_data["password"]) <= 5:
            raise NotAcceptable("the length of the password is short") 

        user = Users(**validated_data)
        
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
        recived_invitations = InvitationSerializer(instance.recived_invitations.all(),many=True)
        sent_invitations = InvitationSerializer(instance.sent_invitations.all(),many=True)
        
        return {
                "id": instance.id,
                "username": instance.username,
                "email": instance.email,
                "phoneNumber": instance.phoneNumber,
                "profilePicture": instance.profilePicture,
                "devices":devices.data,
                "my_devices":my_devices.data,
                "recived_invitations": recived_invitations.data,
                "sent_invitations": sent_invitations.data
                }

          
    


class UserLoginSerializer(serializers.Serializer):
    
    password = serializers.CharField(max_length=20, )
    email = serializers.EmailField()

    def validate(self, data):
        
        try:
            usuario = Users.objects.filter(email=data["email"])[0]
            
            if not check_password(data["password"], usuario.password):
                raise serializers.ValidationError("Email y/o contraseña incorrectos")
        except:  
            raise serializers.ValidationError("Email o contraseña incorrectos")

        return data
    

