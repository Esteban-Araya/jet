from rest_framework import serializers
from .models import Devices

class DevicesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Devices