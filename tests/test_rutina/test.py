from rest_framework.test import APITestCase
from rest_framework import status
from app.models import Users

class TestRutina(APITestCase):

    def setUp(self) -> None:
        self.user = Users.objects.create(
            email = "otroUsuario@gmail.com",
            username = "otroUsuario",
            password = "5678",
        )
        return super().setUp()
    
   
        

    def create_devices(self):
        url = "/device/"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.device = self.client.post(
            url,
            {
                "id" : "9826242",
                "name" : "porton_casa",
                "device_type" : "porton"
            },
            format = 'json'
        )
        self.assertEqual(status.HTTP_201_CREATED,self.device.status_code)
        
    
    def test_create_user(self):
        
        url = "/user/"
        response = self.client.post(
            url,
            {
                "email" : "usuario@gmail.com",
                "username" : "Usuario",
                "password" : "1234",
                "numero" : "+42 3124-12",
                
            },
            format = 'json'
        )
        self.token = response.data["token"]
        self.assertEqual(status.HTTP_201_CREATED,response.status_code)
        
        self.create_devices()

    
        
    


    
    