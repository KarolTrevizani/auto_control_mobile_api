from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class UserCreationTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('users:register-user-list')
        data = {'username': 'testuser', 'email': 'user@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'user@example.com')

    def test_create_user_with_existing_email(self):
        """
        Ensure we cannot create a user with an already registered email.
        """
        User.objects.create_user(username='testuser1', email='user@example.com', password='testpassword123')
        url = reverse('users:register-user-list')
        data = {'username': 'testuser2', 'email': 'user@example.com', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 309)



class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='testpassword123')
        self.url = reverse('login')

    def test_login_success(self):
        """
        Ensure we can log in an existing user and receive a token.
        """
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_login_failure(self):
        """ 
        Ensure login fails with wrong credentials.
        """
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

