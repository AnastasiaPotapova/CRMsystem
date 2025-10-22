from hello import views
from django.urls import path

urlpatterns = [
    path('index/', views.index, name = "home"),
    path('api/users/create/', views.user_create, name='user_create'),
    path('api/users/all/', views.user_list, name='user_list'),
    path('api/users/<str:pk>/', views.user_detail, name='user_detail'),
    path('api/users/<str:pk>/update/', views.user_update, name='user_update'),
    path('api/users/<str:pk>/delete/', views.user_delete, name='user_delete'),
    path('api/visits/create/', views.visit_create, name='visit_create'),
    path('api/visits/all/', views.visit_list_all, name='visit_list_all'),
    path('api/visits/month/', views.visit_list_month, name='visit_list_month'),
    path('api/visits/user/<str:user_id>/', views.visit_list_by_user, name='visit_list_by_user'),
    path('api/users/getname/<str:tg_username>/', views.getname, name='getname'),
]
