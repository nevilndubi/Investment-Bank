from django.db import models

# My models are here.
class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name