from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
