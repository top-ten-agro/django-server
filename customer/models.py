from django.db import models


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=256)
    address = models.TextField(max_length=512)
    phone = models.CharField(max_length=14, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_at']
