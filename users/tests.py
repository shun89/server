from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.password = '123456'
        self.email = 'test@qq.com'

    def test_create(self):
        data = {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass
