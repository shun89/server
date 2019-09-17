from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from .models import User
from .views import UserViewSet


class TokenTests(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.password = '123456'
        User.objects.create_user(
            self.username,
            'test@qq.com',
            self.password
        )

    def test_token_auth(self):
        url = reverse('token-auth')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(APITestCase):
    def setUp(self):
        username = 'test'
        password = '123456'
        email = 'test@qq.com'
        self.user = User.objects.create_user(
            username,
            email,
            password
        )
        url = reverse('token-auth')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create(self):
        data = {
            'username': 'creator',
            'password': '123456',
            'email': 'creator@qq.com'
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        # view = UserViewSet.as_view({'get': 'list'})
        url = reverse('user-set-password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass
