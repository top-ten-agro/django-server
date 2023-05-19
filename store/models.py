from django.db import models
from django.db.models import Q, F
from django.contrib.auth import get_user_model
from product.models import Product
from customer.models import Customer

User = get_user_model()


class Store(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField(max_length=512)
    employees = models.ManyToManyField(
        User, through="StoreRole", related_name='stores')
    products = models.ManyToManyField(
        Product, through="Stock", related_name='stores')
    customers = models.ManyToManyField(
        Customer, through="Balance", related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_at']


class StoreRole(models.Model):
    class Role(models.TextChoices):
        MANAGER = "MANAGER"
        OFFICER = "OFFICER"
        DIRECTOR = "DIRECTOR"

    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='roles')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.OFFICER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.first_name}, {self.role.lower()}, {self.store}"

    class Meta:
        unique_together = ['store', 'user']
        ordering = ['-created_at']


class Stock(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    stock_created = models.DateTimeField(auto_now_add=True)
    stock_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product} - {self.store}"

    class Meta:
        ordering = ['-stock_created']
        unique_together = ['store', 'product']


class Balance(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='balances')
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='balances')
    officer = models.ForeignKey(
        StoreRole,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='officers',
        limit_choices_to=Q(store=F('store')))
    sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_in = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.customer}-{self.store}"

    class Meta:
        unique_together = ['store', 'customer']
        ordering = ['-created_at']
