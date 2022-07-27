from django.db import models

class Employee(models.Model):
    username = models.CharField(max_length=20)
    First_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    
    def __str__(self) -> str:
        return self.First_name
