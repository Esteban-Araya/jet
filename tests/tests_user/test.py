from rest_framework.test import APITestCase
from rest_framework import status

class TestUser(APITestCase):

    def test_registrer_ok(self):
        self.url_registrer = "/user/"

        response = self.client.post(
            self.url_registrer,
            {
                "email" : "usuario@gmail.com",
                "username" : "Usuario",
                "password" : "1234",
                "numero" : "+42 3124-12",
                
            },
            format = 'json'
        )
        

        self.assertEqual(status.HTTP_201_CREATED,response.status_code)

    def test_registrer_fall(self):
        self.url_registrer = "/user/"
        response = self.client.post(
            self.url_registrer,
            {
                "email" : "ksjklnxa",
                "username" : 12314,
                "password" : 234,
                
                
            },
            format = 'json'
        )
        
        
    
        self.assertNotEqual(status.HTTP_201_CREATED,response.status_code)