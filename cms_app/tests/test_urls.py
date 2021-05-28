from rest_framework.test import APISimpleTestCase, APIClient
from django.urls import resolve, reverse
from cms_app.views import RegisterUserView, LoginView, LogoutView, AddContent


class TestUrls(APISimpleTestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, RegisterUserView)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)
    
    # def test_add_content_url_is_resolved(self):
    #     url = reverse('content-list')
    #     print(self.client.get(url))
    #     self.assertEquals(resolve(url).func, AddContent)

