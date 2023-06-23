from django.db import models
from apps.usuarios.models import Users

# Create your models here.
class Devices(models.Model):
    id = models.CharField(max_length=30, primary_key=True, null=False,unique=True)
    name = models.CharField(max_length=40, null=False)
    id_user_main = models.ForeignKey(Users,on_delete=models.CASCADE,  related_name="userMain" )
    device_type = models.CharField(max_length=50, null=False )
    users_id = models.ManyToManyField(Users, related_name="users")
    