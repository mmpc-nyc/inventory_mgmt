from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class TestAuthentication(TestCase):
    fixtures = ['fixtures/test.json', ]

    client = APIClient()
    base_url = 'http://localhost:8000/auth/'
    username = 'test_user'
    email = 'test@email.com'
    password = 'rando90243-slmPas!!'
    user_data = {'username': username, 'password': password}

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password)

    def login_rest(self):
        return self.client.post(urljoin(self.base_url, 'token/login/'), self.user_data)

    def login_jwt(self):
        return self.client.post(urljoin(self.base_url, 'jwt/create/'), self.user_data)

    def test_login(self):
        res = self.login_rest()
        self.assertEqual(res.status_code, 200)

    def test_jwt_create(self):
        res = self.login_jwt()
        self.assertEqual(res.status_code, 200)

    def test_jwt_refresh(self):
        res = self.login_jwt()
        res = self.client.post(urljoin(self.base_url, 'jwt/refresh'), {'refresh': res.data['refresh']})
        self.assertEqual(res.status_code, 200)