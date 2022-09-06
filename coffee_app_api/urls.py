"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.urls import path, include
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', views.coffee_list, name='coffee_list'),
    path('requests/', views.adding, name='adding'),
    path('comments_list/<int:pk>/', views.get_comments, name='get_comments'),
    path('comment_post/', views.comment, name='comment'),
    path('report_page/', views.reportSystem, name='reportSystem'),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
    path('', views.index),
    re_path(r'api/', include('main.urls')),
]