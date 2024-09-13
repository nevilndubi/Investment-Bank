from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# My models are here.
class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True, max_length=100) 
    national_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(validators=[MaxValueValidator(limit_value=datetime.today)])
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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