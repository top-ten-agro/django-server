from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from store.models import Store
from product.models import Product
from customer.models import Customer


User = get_user_model()


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_created')
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total = self.subtotal * (1 - self.commission / 100)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"order id - {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                               MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['order', 'product']
        ordering = ['-created_at']


class Transaction(models.Model):
    class CATEGORIES(models.TextChoices):
        SALES = "SALES"
        TRANSPORT = "TRANSPORT"
        BILL = "BILL"

    category = models.CharField(max_length=30, choices=CATEGORIES.choices)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, null=True, blank=True)
    title = models.CharField(max_length=256)
    note = models.TextField(max_length=1026, null=True, blank=True)
    approved = models.BooleanField(default=False)
    cash_in = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[
        MinValueValidator(0)])
    cash_out = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[
        MinValueValidator(0)])
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_created')
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Restock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='restocks_created')
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='restocks_approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Restock {self.id}"


class RestockItem(models.Model):
    restock = models.ForeignKey(
        Restock, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['restock', 'product']
        ordering = ['-created_at']
