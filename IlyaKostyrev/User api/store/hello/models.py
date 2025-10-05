from django.db import models

# class registre(models.Model):
#     email = models.CharFiels(254)
#     password = models.EmailField()
class Customer(models.Model):
    name= models.CharField(max_length=200,blank=True,null=True)
    email=models.EmailField(max_length=500,blank=True,null=True)
    username=models.CharField(max_length=200,blank=True,null=True)
    location=models.CharField(max_length=200,blank=True,null=True)

class User(models.Model):
    id = models.AutoField(primary_key=True)              
    role = models.CharField(max_length=50)               
    card_id = models.CharField(max_length=100, unique=True)  
    td_username = models.CharField(max_length=150, unique=True) 
    excursions = models.TextField(blank=True)           