from rest_framework import serializers
from .models import Invitations
from rest_framework.exceptions import NotAcceptable


class InvitationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Invitations
        fields = '__all__'

    def validate(self, attrs):
        invitaion = Invitations.objects.filter(reciver=attrs["reciver"], device=attrs["device"])
        if invitaion: 

            raise NotAcceptable({"message":"the invitation already exist"})
        return super().validate(attrs)
    
    

    def to_representation(self, instance):

        return {
            "owner": instance.owner.email,
            "reciver": instance.reciver.email,
            "device": {
                "name":instance.device.name,
                "id": instance.device.id
            }
           
        }