from rest_framework import serializers
from .models import Devices
from django.contrib.auth.hashers import make_password,check_password

class DevicesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Devices