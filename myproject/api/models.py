from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# My models are here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=100) 
    phone_number = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    area_of_residence = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(validators=[MaxValueValidator(limit_value=date.today)])
    age = models.IntegerField()
    place_of_work = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.first_name} {self.surname} {self.last_name}")

class Branch (models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=250)
    branch_code = models.CharField(max_length=10, unique=True)
    
    class Meta:
        verbose_name_plural = "Branches"

    def json_object(self):
        return {
            "name ": self.name,
            "address": self.address,
            "branch_code": self.branch_code
        }
    
    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def json_object(self):
        return {
            "name": self.name,
            "branch": self.branch
        } 
    
    def __str__(self):
        return self.name

class InvestmentAccount(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='UserInvestmentAccount')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserInvestmentAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_post = models.BooleanField(default=False)
    can_crud = models.BooleanField(default=False)