from hello import views
from django.urls import path

urlpatterns = [
    path('api/users/create/', views.user_create, name='user_create'),# Создание пользователя
    path('api/users/all/', views.user_list, name='user_list'),# Получение списка всех пользователей
    path('api/users/<str:pk>/', views.user_detail, name='user_detail'),# Получение деталей пользователя по pk
    path('api/users/<str:pk>/update/', views.user_update, name='user_update'),# Обновление пользователя по pk
    path('api/users/<str:pk>/delete/', views.user_delete, name='user_delete'),# Удаление пользователя по pk
    path('api/visits/create/', views.visit_create, name='visit_create'),# Создание нового посещения
    path('api/visits/all/', views.visit_list_all, name='visit_list_all'),# Получение списка всех посещений
    path('api/visits/month/', views.visit_list_month, name='visit_list_month'),# Получение списка посещений за указанный месяц и год, с опциональной фильтрацией по user_id
    path('api/visits/user/<str:user_id>/', views.visit_list_by_user, name='visit_list_by_user'),# Получение списка посещений по user_id
    path('api/users/getname/<str:tg_username>/', views.getname, name='getname'),# Получение fullname по td_username
    path('api/visits/<str:visit_id>/delete/', views.visit_delete, name='visit_delete'),# Удаление посещения по id
]
