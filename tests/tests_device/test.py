from rest_framework.test import APITestCase
from rest_framework import status

class TestUser(APITestCase):
    url = "/device/"
    def create_device(self):

        response = self.client.post(
            self.url, 
            {
                "id":"23412414",
                "name":"mi_porton",
                "device_type":"porton"
            },
            format = 'json'
        )
       
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)