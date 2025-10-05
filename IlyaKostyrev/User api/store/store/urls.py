
from hello import views
from django.urls import path

urlpatterns = [
    path('index/', views.index, name = "home"),
    path('reg/', views.registration, name = "reg.html"),
    path('api/users/create' , views.user_create, name='user_create'),
    path('api/users/all' , views.user_list, name='user_list'),
    path('api/users/<int:pk>' , views.user_detail, name='user_detail'),
    path('api/users/<int:pk>/update' , views.user_update, name='user_update'),
    path('api/users/<int:pk>/delete' , views.user_delete, name='user_delete'),
]
