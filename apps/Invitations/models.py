from django.db import models
from apps.Devices.models import Devices
from apps.Users.models import Users
# Create your models here.
class Invitations(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="sent_invitations")
    reciver = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="recived_invitations")
    device = models.ForeignKey(Devices, on_delete=models.CASCADE,related_name="device")