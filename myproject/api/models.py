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
    password = models.CharField(max_length=128, default=make_password('temporary_password'))  # Increased Length for better security
    national_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(validators=[MaxValueValidator(limit_value=datetime.today)])
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name