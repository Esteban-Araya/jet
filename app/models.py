from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


from django.contrib.auth.hashers import make_password
from uuid import uuid4
# Create your models here.

class UserManagers(BaseUserManager):
    def _create_user(self,username, password,email,is_staff,is_superuser,**extra_fields):
        if not email:
            raise ValueError('No hay correo electronico')
        
        usuario = self.model(
            username = username,
            email = email, 
            is_staff = is_staff,
            is_superuser =is_superuser,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_user(self,username,email, password=None,**extra_fields):
        return self._create_user(username, password,email,False,False,**extra_fields)
    
    def create_superuser(self,username,email, password=None,**extra_fields):
        return self._create_user(username, password,email,True,True,**extra_fields)

class Users(AbstractBaseUser):
    id = models.UUIDField(primary_key=True,default=uuid4, editable=False)
    username = models.CharField(max_length=20, null=False)
    #password = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False ,unique=True)
    phoneNumber = models.CharField(max_length=15, null=True)
    profilePicture = models.TextField(default=None, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManagers()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']


class Devices(models.Model):
    id = models.CharField(max_length=30, primary_key=True, null=False,unique=True)
    name = models.CharField(max_length=40, null=False)
    id_user_main = models.ForeignKey(Users,on_delete=models.CASCADE,  related_name="my_devices" )
    device_type = models.CharField(max_length=50, null=False )
    users_id = models.ManyToManyField("Users", related_name="devices", null=True)
