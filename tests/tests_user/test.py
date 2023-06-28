from rest_framework.test import APITestCase
from rest_framework import status

class TestUser(APITestCase):
    token = ""
    url = "/registrer/"

    def get_user(self):

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(self.url)
        
        self.assertEqual('Usuario',response.data["username"])
    
    def test_registrer_ok(self):
        

        response = self.client.post(
            self.url,
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
        
        self.get_user()

    def test_registrer_fall(self):

        response = self.client.post(
            self.url,
            {
                "username" : 12314,
                "password" : 234
                
                
            },
            format = 'json'
        )
    
        self.assertNotEqual(status.HTTP_201_CREATED,response.status_code)

    
    