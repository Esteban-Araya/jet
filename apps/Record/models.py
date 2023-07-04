from django.db import models
from apps.Users.models import Users
from apps.Devices.models import Devices

# Create your models here.
class Record(models.Model):
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE,  related_name="record" )
    device_id = models.ForeignKey(Devices,on_delete=models.CASCADE,  related_name="record")
    state = models.BooleanField(null=False, default=False)
    time = models.DateTimeField(auto_now_add=True)
