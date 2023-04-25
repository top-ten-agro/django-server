from django.db import models
from store.models import Store
from product.models import Product
from user.models import Employee
from customer.models import Customer


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, through='OrderItem', related_name='orders')
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

class Transaction(models.Model):

    class TYPES(models.TextChoices):
        IN = "IN"
        OUT = "OUT"

    class CATEGORIES(models.TextChoices):
        RECOVERY = "RECOVERY"
        TRANSPORT = "TRANSPORT"
        BILL = "BILL"

    type = models.CharField(max_length=3, choices=TYPES.choices)
    category = models.CharField(max_length=30, choices=CATEGORIES.choices)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256)
    note = models.TextField(max_length=1026, null=True, blank=True)
    approved = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
