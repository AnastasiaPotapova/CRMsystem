from django.urls import path
from . import views

urlpatterns = [
    path('excursions/', views.ExcursionListCreateView.as_view(), name='excursion-list-create'),
    path('excursions/<int:pk>/', views.ExcursionDetailView.as_view(), name='excursion-detail'),
    path('polls/', views.PollListCreateView.as_view(), name='poll-list-create'),
    path('polls/<int:pk>/', views.PollDetailView.as_view(), name='poll-detail'),
]