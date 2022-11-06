from django.contrib.auth.models import User
from django.db import models


#Модель Кофейни
class CoffeeShop(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default=None)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to="coffee", null=True)
    rating = models.FloatField(default=0)
    numRates = models.IntegerField(default=0)


#Модель комментариев
class Comment(models.Model):
    author = models.CharField(max_length=255)
    text = models.CharField(max_length=255, default=None)
    coffee_shop = models.ForeignKey(to=CoffeeShop, on_delete=models.CASCADE)


#модель жалоб
class Reports(models.Model):
    report = models.CharField(max_length=255, default=None)
    coffee_shop = models.ForeignKey(to=CoffeeShop, on_delete=models.CASCADE)


#модель статуса пользователя
class Owners(models.Model):
    username = models.CharField(max_length=255)
    is_Owner = models.CharField(max_length=255)


class Info(models.Model):
    shop_id = models.IntegerField(default=0)
    info = models.CharField(max_length=255, default=None)


class Favourite(models.Model):
    shop_id = models.IntegerField(default=0)
    username = models.CharField(max_length=255, default=None)
    shop_name = models.CharField(max_length=255, default=None)