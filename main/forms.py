from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import CoffeeShop, Comment, Reports, Owners, Info


#Форма информации о кофейне
class AddForm(forms.Form):
    class Meta:
        model = CoffeeShop
        fields = ['name', 'description', 'latitude', 'longitude']


#Форма информации о комментариях
class AddComment(forms.Form):
    class Meta:
        model = Comment
        fields = ['text', 'author', 'coffee_shop']


#Форма информации о жалобах
class Reports(forms.Form):
    class Meta:
        model = Reports
        fields = ['report', 'coffee_shop']


#Форма информации о пользователе
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#Форма информации о статусе пользователя
class OwnerAdd(forms.Form):
    class Meta:
        model = Owners
        fields = ['username', 'is_Owner']


class InfoAdd(forms.Form):
    class Meta:
        model = Info
        fields = ['shop_id', 'info']