from django.urls import reverse
from django.test import TestCase
from .models import User
from rest_framework.test import APITestCase
from rest_framework import status

class UserModelTest(TestCase):
    def test_user_picker_filter(self):
        user1 = User(
            username    = 'test@yahoo.com',
            password    = 'asdf',
            name        = 'Edgar',
            lastname    = 'Ceron',
            active      = True,
            profile     = None,
            needPassword= True
        )

        user2 = User(
            username    = 'test2@yahoo.com',
            password    = 'asdf',
            name        = 'Edgar',
            lastname    = 'Florez',
            active      = True,
            profile     = None,
            needPassword= True
        )

        user3 = User(
            username    = 'test3@yahoo.com',
            password    = 'asdf',
            name        = 'Mauricio',
            lastname    = 'Florez',
            active      = True,
            profile     = None,
            needPassword= True
        )

        user1.save()
        user2.save()
        user3.save()

        q  = list(User.usersPickerFilter('Edgar'))
        q2 = list(User.usersPickerFilter('Mauricio'))
        q3 = list(User.usersPickerFilter('x'))
        self.assertEqual(q, [user1, user2])
        self.assertEqual(q2, [user3])
        self.assertEqual(q3, [])
# Create your tests here.

class UserWevserviceTest(TestCase):
    def test_picker_search_user(self):
        user1 = User(
            username    = 'test@yahoo.com',
            password    = 'asdf',
            name        = 'Edgar',
            lastname    = 'Ceron',
            active      = True,
            profile     = None,
            needPassword= True
        )

        user2 = User(
            username    = 'asdfg@yahoo.com',
            password    = 'asdf',
            name        = 'Edgar',
            lastname    = 'Ceron',
            active      = True,
            profile     = None,
            needPassword= True
        )
        user1.save()
        user2.save()
        
        url       = reverse('picker_list')
        data      = {'value':'Edgar'}
        response  = self.client.post(url, data, format='json')
        result    = response.data['result']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(result[0])['username'],user1.username)
        self.assertEqual(dict(result[1])['username'],user2.username)

    def test_picker_search_user_limit(self):
        for x in range(20):
            aux = User(
                username    = 'test' + str(x) + '@yahoo.com',
                password    = 'asdf',
                name        = 'test',
                lastname    = 'test',
                active      = True,
                profile     = None,
                needPassword= True
            )
            aux.save()
            aux = None
        
        url       = reverse('picker_list')
        data      = {'value':'test'}
        response  = self.client.post(url, data, format='json')
        result    = response.data['result']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result),10)
