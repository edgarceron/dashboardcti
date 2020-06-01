""" Tests for profile module """
import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from .models import Profile, Action, App
from rest_framework.test import APITestCase


class ProfileWebserviceTest(TestCase):
    """ Webservices test class"""
    def test_picker_search_profile(self):
        """ Check profile picker search by a text value and not selecting inactive profiles"""
        profile_a = Profile(
            name="Admin",
            active=True
        )

        profile_b = Profile(
            name="AdminInactive",
            active=False
        )

        profile_c = Profile(
            name="Usuario",
            active=False
        )

        profile_a.save()
        profile_b.save()
        profile_c.save()

        url = reverse('picker_list_profile')
        data = {'value':'Adm'}
        response = self.client.post(url, data, format='json')
        result = response.data['result']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(result[0])['name'], profile_a.name)
        self.assertEqual(len(result), 1)

    def test_profile_form(self):
        """ Checks if actions by app context is correct"""
        app_a = App(name="Usuarios")
        app_a.save()
        app_b = App(name="Perfiles")
        app_b.save()
        app_c = App(name="Dashboard")
        app_c.save()

        action_a = Action(name='create_user', label="", app=app_a)
        action_b = Action(name='delete_user', label="", app=app_a)
        action_c = Action(name='create_profile', label="", app=app_b)
        action_d = Action(name='get_tmo', label="", app=app_c)

        action_a.save()
        action_b.save()
        action_c.save()
        action_d.save()

        url = reverse('create_profile')
        response = self.client.get(url, format='json')
        actions_by_app = response.context['result']

        self.assertEqual(len(actions_by_app), 3)

        for app in actions_by_app:
            if app['id'] == app_a.id:
                actions = app['actions']
                break

        self.assertEqual(len(actions), 2)
        
    def test_profile_add(self):
        app_a = App(name="Usuarios")
        app_a.save()
        app_b = App(name="Perfiles")
        app_b.save()
        app_c = App(name="Dashboard")
        app_c.save()

        action_a = Action(name='create_user', label="", app=app_a)
        action_b = Action(name='delete_user', label="", app=app_a)
        action_c = Action(name='create_profile', label="", app=app_b)
        action_d = Action(name='get_tmo', label="", app=app_c)

        action_a.save()
        action_b.save()
        action_c.save()
        action_d.save()
        actions = []
        actions.append({'action':action_a.id, 'permission': True})
        actions.append({'action':action_b.id, 'permission': True})
        
        data = {
            'name':'Admin',
            'active': True,
            'actions': json.dumps(actions)
        }

        url = reverse('add_profile')
        response = self.client.post(url, data, format='json')
        success = response.data['success']
        self.assertEqual(success, True)