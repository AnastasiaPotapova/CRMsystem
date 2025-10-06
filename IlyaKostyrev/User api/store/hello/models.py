from django.db import models

## Эта модель была создана для примера и тестов
## В реальном проекте она может быть не нужна
## Пока удалять её не буду так как уже поздно и мне лень
## Если что потом удалю
class Customer(models.Model):
    name= models.CharField(max_length=200,blank=True,null=True)
    email=models.EmailField(max_length=500,blank=True,null=True)
    username=models.CharField(max_length=200,blank=True,null=True)
    location=models.CharField(max_length=200,blank=True,null=True)

class User(models.Model):
    id = models.CharField(max_length =200, primary_key=True, unique=True)              
    role = models.CharField(max_length=50)               
    card_id = models.CharField(max_length=100, unique=True)  
    td_username = models.CharField(max_length=150, unique=True) 
    excursions = models.TextField(blank=True)           