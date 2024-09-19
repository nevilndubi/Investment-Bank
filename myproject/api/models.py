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
    ACCOUNT_TYPE_CHOICES = [
        ('Investment Account 1', 'Investment Account 1'),
        ('Investment Account 2', 'Investment Account 2'),
        ('Investment Account 3', 'Investment Account 3'),  
    ]

    account_type = models.CharField(max_length=100, choices=ACCOUNT_TYPE_CHOICES)
    account_number = models.CharField(max_length=20, unique=True, blank=True)
    users = models.ManyToManyField(User, related_name='investment_accounts', blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transactions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.account_number:
            prefix = ''
            if self.account_type == 'Investment Account 1':
                prefix = 'invacc1-'
            elif self.account_type == 'Investment Account 2':
                prefix = 'invacc2-'
            elif self.account_type == 'Investment Account 3':
                prefix = 'invacc3-'
            
            last_account = InvestmentAccount.objects.filter(account_type=self.account_type).order_by('id').last()
            if last_account:
                last_serial = int(last_account.account_number.split('-')[-1])
                new_serial = last_serial + 1
            else:
                new_serial = 1
            
            self.account_number = f"{prefix}{new_serial:03d}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Investment Account Type: {self.account_type}"

class UserInvestmentAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)

class Transfer(models.Model):
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.amount} to {self.branch.name} on {self.date}"

class Withdraw(models.Model):
    amount = models.FloatField()
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Withdraw of {self.amount}"

class Deposit(models.Model):
    amount = models.FloatField()
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Deposit of {self.amount}"