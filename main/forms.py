from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import CoffeeShop, Comment, Reports


class AddForm(forms.Form):
    class Meta:
        model = CoffeeShop
        fields = ['name', 'description', 'latitude', 'longitude']


class AddComment(forms.Form):
    class Meta:
        model = Comment
        fields = ['text', 'author', 'coffee_shop']


class Reports(forms.Form):
    class Meta:
        model = Reports
        fields = ['report', 'coffee_shop']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
