from django.db import models

# My models are here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name