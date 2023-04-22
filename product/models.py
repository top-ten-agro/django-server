from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256)
    group_name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    published = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_at']
