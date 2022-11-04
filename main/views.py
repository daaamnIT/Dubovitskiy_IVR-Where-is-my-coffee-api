from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import CreateUserForm
from django.core.serializers import serialize
from django.http import HttpResponse
from .forms import AddForm
from .forms import AddComment
from .forms import Reports
from .forms import OwnerAdd
from .forms import InfoAdd
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import CreateUserSerializer
from django.contrib.auth.models import User


#вью функция страницы входа (не используется)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


#вью ф-ия выхода из профиля (не используется)
def logoutUser(request):
    logout(request)
    return redirect('login')


#вью ф-ия страницы регистрации (не используется)
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


#вью ф-ия получения списка кофеен
def coffee_list(request):
    coffeelist = CoffeeShop.objects.all()
    data = serialize("json", coffeelist, indent=2)
    return HttpResponse(data, content_type="application/json")      #возвращает json


#вью ф-ия главной страницы
def index(request):
    return render(request, 'index.html')      #возвращает страницу


#вью-фия добавления кофейни в бд
@csrf_exempt
def adding(request):
    if request.method == 'POST':
        f = AddForm(request.POST)
        if f.is_valid():
            name = f.data['name']
            description = f.data['description']
            latitude = f.data['latitude']
            longitude = f.data['longitude']

            item = CoffeeShop(name=name, description=description, latitude=latitude, longitude=longitude)
            item.save()

            coffee_list(request)

    return HttpResponse(request)      #возвращает ответ (ок/не ок)


#вью ф-ия добавления комментов в бд
@csrf_exempt
def comment(request):
    if request.method == 'POST':
        f = AddComment(request.POST)
        if f.is_valid():
            text = f.data['text']
            author = f.data['author']
            coffee_shop_id = f.data['coffee_shop_id']
            coffee_shop = CoffeeShop.objects.get(id=coffee_shop_id)
            item = Comment(text=text, author=author, coffee_shop=coffee_shop)
            item.save()
        else:
            print(f.errors)

    return HttpResponse(request)      #возвращает ответ(ок/не ок)


#вью ф-ия получения списка комментов
def get_comments(request, pk):
    comments = Comment.objects.filter(coffee_shop=pk)
    data = serialize("json", comments, indent=2)
    return HttpResponse(data, content_type="application/json")      #возвращает json


#ф-ия добавления репортов в бд
@csrf_exempt
def reportSystem(request):
    if request.method == 'POST':
        f = Reports(request.POST)
        if f.is_valid():
            report = f.data['report']
            coffee_shop_id = f.data['coffee_shop_id']
            coffee_shop = CoffeeShop.objects.get(id=coffee_shop_id)
            item = Reports(text=report, coffee_shop=coffee_shop)
            item.save()
        else:
            print(f.errors)

    return HttpResponse(request)      #возвращает ответ (ок/не ок)


#класс создания юзера с использованием Django Rest Framework
class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(                              #возвращает токен пользователя и ответ
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )



#класс выхода пользователя из аккаунта (DRF)
class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)        #возвращает ответ


#класс получения комментов
class CommentsView(APIView):
    def get(self, request, pk):
        comments = Comment.objects.filter(coffee_shop=pk)
        data = serialize("json", comments, indent=2)
        return HttpResponse(data, content_type="application/json")      #возвращает json


#ф-ия получения информации о пользователе
class UserInfo(APIView):
    def get(self, request):
        name = request.user
        info = User.objects.filter(username=name)
        data = serialize("json", info, indent=2)
        return HttpResponse(data, content_type="application/json")      #возвращает json


#ф-ия добавления статуса пользователя в бд
@csrf_exempt
def setStatus(request):
    if request.method == 'POST':
        f = OwnerAdd(request.POST)
        if f.is_valid():
            username = f.data['username']
            status = f.data['is_Owner']
            item = Owners(username=username, is_Owner=status)
            item.save()
        else:
            print(f.errors)

    return HttpResponse(request)      #возвращает ответ


#ф-ия получения статуса пользователя
class UserStatus(APIView):
    def get(self, request):
        name = request.user
        info = Owners.objects.filter(username=name)
        data = serialize("json", info, indent=2)
        print(data)
        return HttpResponse(data, content_type="application/json")      #возвращает json

#
#
# @csrf_exempt
# def RatingSys(request):
#     if request.method == 'POST':
#         f = AddComment(request.POST)
#         if f.is_valid():
#             username = f.data['username']
#             status = f.data['is_Owner']
#             item = Owners(username=username, is_Owner=status)
#             item.save()
#         else:
#             print(f.errors)
#
#     return HttpResponse(request)


#ф-ия получения рейтинга кофейни
class getRating(APIView):
    def get(self, request, pk):
        rates = CoffeeShop.objects.filter(id=pk)
        data = serialize("json", rates, indent=2)
        return HttpResponse(data, content_type="application/json")      #возвращает json


#ф-ия добавления рейтинга в бд
@csrf_exempt
def setRating(request):
    if request.method == 'POST':
        f = AddComment(request.POST)
        if f.is_valid():
            pk = f.data['coffee_shop_id']
            shop = list(CoffeeShop.objects.filter(id=pk).values())
            number = shop[0]['numRates']
            rating = shop[0]['rating']
            total_rate = number * rating
            new_total_rate = total_rate + int(f.data['rate'])
            new_number = number + 1
            new_total_rate /= new_number
            CoffeeShop.objects.filter(id=pk).update(numRates=new_number)
            CoffeeShop.objects.filter(id=pk).update(rating=new_total_rate)
        else:
            print(f.errors)

    return HttpResponse(request)      #возвращает ответ


#
def rating_list(request):
    coffeelist = CoffeeShop.objects.order_by('-rating')
    data = serialize("json", coffeelist, indent=2)
    return HttpResponse(data, content_type="application/json")      #возвращает json

#
# class AddInfo(APIView):
#     def update(self, request):
#         f = InfoAdd(request.POST)
#         if f.is_valid():
#             shop_id = f.data['shop_id']
#             info = f.data['info']
#             print(info)
#             item = Info(shop_id=shop_id, info=info)
#             item.save()
#
#         return HttpResponse(request)  # возвращает ответ (ок/не ок)




@csrf_exempt
def AddInfo(request):
    if request.method == 'POST':
        f = InfoAdd(request.POST)
        if f.is_valid():
            a = []
            for i in range(len(request.POST)-1):
                print(f.data['info_'+str(i)])
                a.append(f.data['info_'+str(i)])
            print(a)
            res = []
            print(Info.objects.filter(shop_id=int(f.data['shop_id'])).count())
            if Info.objects.filter(shop_id=int(f.data['shop_id'])).count() == 0:
                for i in range(len(a)):
                    shop_id = f.data['shop_id']
                    info = a[i]
                    item = Info(shop_id=shop_id, info=info)
                    item.save()
            else:
                values = list(Info.objects.filter(shop_id=int(f.data['shop_id'])).values_list('info', flat=True))
                print(values)
                for i in range(len(a)):
                    if a[i] not in values:
                        res.append(a[i])
            if len(res) == 0:
                print('nothing')
            else:
                print('opa')
                for i in range(len(res)):
                    shop_id = f.data['shop_id']
                    info = res[i]
                    item = Info(shop_id=shop_id, info=info)
                    item.save()

        return HttpResponse(request)  # возвращает ответ (ок/не ок)


def info_list(request, pk):
    infolist = Info.objects.filter(shop_id=pk)
    data = serialize("json", infolist, indent=2)
    return HttpResponse(data, content_type="application/json")      #возвращает json