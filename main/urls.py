from django.urls import re_path, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateUserAPIView, LogoutUserAPIView, CommentsView, UserInfo, UserStatus, getRating, AddInfo


#ссылки использующие DRF Token для авторизации пользователя
urlpatterns = [
    re_path(r'^auth/login/$',
            obtain_auth_token,
            name='auth_user_login'),
    re_path(r'^auth/register/$',
            CreateUserAPIView.as_view(),
            name='auth_user_create'),
    re_path(r'^auth/logout/$',
            LogoutUserAPIView.as_view(),
            name='auth_user_logout'),
    path('comments_list/<pk>/',
         CommentsView.as_view(),
         name='comments_list',
         ),
    path('me/',
         UserInfo.as_view(),
         name='getUserInfo',
         ),
    path('status/',
         UserStatus.as_view(),
         name='getUserStatus',
         ),
    path('rates/<pk>',
         getRating.as_view(),
         name='getRating',
         ),
    # path('infoadd/',
    #      AddInfo.as_view(),
    #      name="InfoAdding"
    #      ),
]
