from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .serializers import UserSerializer


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
        self.client.force_authenticate(user=self.user)

    def test_create(self):
        data = {
            'username': 'creator',
            'password': '123456',
            'email': 'creator@qq.com'
        }
        url = reverse('users:user-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        url = reverse('users:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        url = reverse('users:user-detail', args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse('users:user-detail', args=(self.user.pk,))
        data = UserSerializer(self.user).data
        data['email'] = 'update@qq.com'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        url = reverse('users:user-detail', args=(self.user.pk,))
        data = {
            'username': 'test123'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        url = reverse('users:user-detail', args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
