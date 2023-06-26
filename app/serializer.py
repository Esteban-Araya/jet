from rest_framework import serializers
from .models import Users, Devices, Record
from django.contrib.auth.hashers import make_password,check_password


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
        # print(DevicesSerializer(instance.devices.all()]).data)
        # for i in range(len(instance.devices.all())):
            
        #     devices.append(DevicesSerializer(instance.devices.all()[i]).data)

        # for i in range(len(instance.my_devices.all())):
            
        #     my_devices.append(DevicesSerializer(instance.my_devices.all()[i]).data)
            
        
        return {
                "id": instance.id,
                "username": instance.username,
                "email": instance.email,
                "phoneNumber": instance.phoneNumber,
                "profilePicture": instance.profilePicture,
                "devices":devices.data,
                "my_devices":my_devices.data
                }
    

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
        #exclude = ["id_user_main","id" ]
        fields = '__all__'

        model = Devices

class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Record