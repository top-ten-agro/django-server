from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Employee(models.Model):
    class Designation(models.TextChoices):
        OFFICER = "OFFICER"
        MANAGER = "MANAGER"
        DIRECTOR = "DIRECTOR"

    name = models.CharField(max_length=200)
    designation = models.CharField(
        max_length=10, choices=Designation.choices, default=Designation.OFFICER)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
