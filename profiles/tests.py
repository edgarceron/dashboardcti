""" Tests for profile module """
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from .models import Profile
from rest_framework.test import APITestCase


class UserWebserviceTest(TestCase):
    """ Webservices test class"""
    def test_picker_search_user(self):
        """ Check profile picker search by a text value and not selecting inactive profiles"""
        profilea = Profile(
            name="Admin",
            active=True
        )

        profileb = Profile(
            name="AdminInactive",
            active=False
        )

        profilec = Profile(
            name="Usuario",
            active=False
        )

        profilea.save()
        profileb.save()
        profilec.save()

        url = reverse('picker_list_profile')
        data = {'value':'Adm'}
        response = self.client.post(url, data, format='json')
        result = response.data['result']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(result[0])['name'], profilea.name)
        self.assertEqual(len(result), 1)

# Create your tests here.
