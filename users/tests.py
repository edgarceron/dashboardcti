from django.urls import reverse
from django.test import TestCase
from .models import User
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import LoginSession

class UserModelTest(TestCase):
    def test_user_picker_filter(self):
        """ Test if the returned list get the correct elements"""
        user1 = User(
            username='test@yahoo.com',
            password='asdf',
            name='Edgar',
            lastname='Ceron',
            active=True,
            profile=None,
            need_password=True
        )

        user2 = User(
            username='test2@yahoo.com',
            password='asdf',
            name='Edgar',
            lastname='Florez',
            active=True,
            profile=None,
            need_password=True
        )

        user3 = User(
            username='test3@yahoo.com',
            password='asdf',
            name='Mauricio',
            lastname='Florez',
            active=True,
            profile=None,
            need_password= True
        )

        user1.save()
        user2.save()
        user3.save()

        query = list(User.usersPickerFilter('Edgar'))
        query2 = list(User.usersPickerFilter('Mauricio'))
        query3 = list(User.usersPickerFilter('x'))
        self.assertEqual(query, [user1, user2])
        self.assertEqual(query2, [user3])
        self.assertEqual(query3, [])


class UserWebserviceTest(TestCase):
    def test_picker_search_user(self):
        user1 = User(
            username = 'test@yahoo.com',
            password = 'asdf',
            name = 'Edgar',
            lastname = 'Ceron',
            active = True,
            profile = None,
            need_password = True
        )

        user2 = User(
            username = 'asdfg@yahoo.com',
            password = 'asdf',
            name = 'Edgar',
            lastname = 'Ceron',
            active = True,
            profile = None,
            need_password = True
        )
        user1.save()
        user2.save()
        
        url = reverse('picker_list_user')
        data = {'value':'Edgar'}
        response = self.client.post(url, data, format='json')
        result = response.data['result']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(result[0])['username'], user1.username)
        self.assertEqual(dict(result[1])['username'], user2.username)

    def test_picker_search_user_limit(self):
        for x in range(20):
            aux = User(
                username    = 'test' + str(x) + '@yahoo.com',
                password    = 'asdf',
                name        = 'test',
                lastname    = 'test',
                active      = True,
                profile     = None,
                need_password= True
            )
            aux.save()
            aux = None

        url = reverse('picker_list_user')
        data = {'value':'test'}
        response = self.client.post(url, data, format='json')
        result = response.data['result']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 10)

    def test_delete_user_test(self):
        user1 = User(
            username='test@yahoo.com',
            password='asdf',
            name='Edgar',
            lastname='Ceron',
            active=True,
            profile=None,
            need_password=True
        )
        user1.save()

        url = reverse('delete_user', args=[user1.id])
        self.client.get(url)
        search = list(User.objects.filter(id=1))

        self.assertEqual(search, [])

    def test_login_user(self):
        user1 = {
            'username':'test@yahoo.com',
            'password':'password',
            'name':'Edgar',
            'lastname':'Ceron',
            'active':True,
            'profile':'',
        }

        url_set = reverse('add_user')
        response = self.client.post(url_set, user1, format='json')
        self.assertEqual(True, True)
        created = response.data['success']
        self.assertEqual(created, True)

        url = reverse('login')
        data = {'username':'test@yahoo.com', 'password':'password'}       
        response = self.client.post(url, data, format='json')
        result = response.data['success']
        self.assertEqual(result, True)

        key = response.data['key']
        try:
            found = True
            LoginSession.objects.get(key=key)
        except:
            found = False

        self.assertTrue(found)

        data = {'username':'test@yahoo.com', 'password':'wrongpassword'}       
        response2 = self.client.post(url, data, format='json')
        result2 = response2.data['success']
        self.assertEqual(result2, False)
