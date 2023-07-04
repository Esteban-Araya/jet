from rest_framework import serializers
from .models import Record

class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Record

    def to_representation(self, instance):
        return {
            "time": instance.time,
            "state": instance.state,
            "user": instance.user_id.username
        }