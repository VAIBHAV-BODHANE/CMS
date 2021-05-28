from rest_framework import response
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from cms_app.models import UserRegister, ContentItem
from rest_framework import status
from rest_framework.authtoken.models import Token
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class TestRegister(APITestCase):
    # list_url = reverse('login')

    # def setUp(self):
    #     self.user = self.test_user_register()
    #     print(self.user)
    #     self.token = Token.objects.get(user=self.user)
    
    def test_user_register(self):
        data = {'email': 'sachin@gmail.com', 'full_name': 'Sachin Chaudhar', 'phone': '8785545655', 'pincode': '400080', 'password': 'sachin@123'}
        
        response = self.client.post("/cms/register/", data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    # def test_user_login(self):
    #     data = {'email': 'apexdead@gmail.com', 'password': 'apexdead'}
        
    #     response = self.client.post("/cms/login/", data)
    #     self.assertEquals(response.status_code, status.HTTP_200_OK)


class TestUserContent(APITestCase):

    list_url = reverse('content-list')

    def setUp(self):
        # self.user = UserRegister.objects.create_user(email='chetan@gmail.com', full_name='chetan nirmal', phone='8799986799', pincode="400080", password="cheatn@123")
        self.user = UserRegister.objects.create_user(email='chetan@gmail.com', full_name='chetan nirmal', phone='8799986799', password="cheatn@123")
        self.token = Token.objects.get(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_authenticate(self):
        # data={'email': 'chetan@gmail.com', 'password': 'cheatn@123'}
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_un_authenticate(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_retrive_user_content(self):
        #add test
        with open(os.path.join(BASE_DIR, 'media/cms_app/pdf_document/2021/05/28/fomr1.pdf'), 'rb') as fp:
            data = {'title': 'test', 'body': 'test', 'summary': 'this is test', 'document': fp }
            response = self.client.post("/cms/content/", data)
            self.assertEquals(response.status_code, status.HTTP_201_CREATED)


        # Retrive test
        response2 = self.client.get(reverse("content-detail",kwargs={'pk':1}))
        self.assertEquals(response2.status_code, status.HTTP_200_OK)
        self.assertEquals(UserRegister.objects.get(id=response2.data['user']).email, 'chetan@gmail.com')

        pdf = response2.data['document']

        # {'id': 1, 'user': 1, 'title': 'test', 'body': 'test', 'summary': 'this is test', 'document': 'http://testserver/media/cms_app/pdf_document/2021/05/28/fomr1_6iaslLj.pdf', 'category': ''}

        # Update test
        response3 = self.client.patch(reverse("content-detail",kwargs={'pk':1}), {'category': 'test'})
        self.assertEquals(response3.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response3.content), {'id': 1, 'user': 1, 'title': 'test', 'body': 'test', 'summary': 'this is test', 'document': pdf, 'category': 'test'})

        # Delete test
        response4 = self.client.delete(reverse("content-detail",kwargs={'pk':1}))
        self.assertEquals(response4.status_code, status.HTTP_204_NO_CONTENT)


    def test_user_logout(self):
        response = self.client.post("/cms/logout/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
