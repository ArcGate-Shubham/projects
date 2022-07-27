#from pydoc import cli
from django.test import TestCase, Client
from django.urls import reverse
from applogin.models import Employee
import unittest

class TestViews(TestCase):
    def test_sign_up_GET(self):
        client = Client()

        response =client.get(reverse('signup'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_log_in_GET(self):
        client = Client()

        response = client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
