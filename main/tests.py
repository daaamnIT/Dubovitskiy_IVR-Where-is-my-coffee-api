from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from main.models import CoffeeShop, Comment, Reports, Owners, Info, Favourite, Menu, Preorder
import json


# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.comments_url = reverse('get_comments', args=[1])
        self.comments_url2 = reverse('get_comments', args=[10])
        self.comments_url3 = reverse('getUserStatus')
        self.comments_url4 = reverse('GetOrders')

        CoffeeShop.objects.create(
            name='testname',
            description='test_desc',
            latitude=55.14,
            longitude=15.123,
            rating=5,
            numRates=10,
            hasOwner='True',
            OwnerName='TestOwner'
        )
        Comment.objects.create(
            author='test',
            text='test_text',
            coffee_shop_id=1
        )
        self.owners = Owners.objects.create()

    def test_coffee_list_GET(self):                         #тест получения списка кофеен
        response = self.client.get(reverse('coffee_list'))
        self.assertEquals(response.status_code, 200)

    def test_comments_list_GET_status_200(self):           #тест получения списка комментариев для существующей кофейни
        response = self.client.get(self.comments_url)
        self.assertEquals(response.status_code, 200)

    def test_comments_list_GET_status_200(self):            #тест получения списка комментариев для несуществующей кофейни (сервер не падает)
        response = self.client.get(self.comments_url2)
        self.assertEquals(response.status_code, 200)

    def test_GET_user_status_401(self):                 #тест получения статсу пользователя (пользователь не авторизован)
        response = self.client.get(self.comments_url3)
        self.assertEquals(response.status_code, 401)

    def test_GET_user_status_401(self):                 #тест получения предзаказов неавторизованным пользователем
        response = self.client.get(self.comments_url4)
        self.assertEquals(response.status_code, 401)

