from django.db import models
from django.db.models import Q, F
from django.contrib.auth import get_user_model
from product.models import Product
from customer.models import Customer

User = get_user_model()


class Depot(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField(max_length=512)
    employees = models.ManyToManyField(
        User, through="DepotRole", related_name='depots')
    products = models.ManyToManyField(
        Product, through="Stock", related_name='depots')
    customers = models.ManyToManyField(
        Customer, through="Balance", related_name='depots')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_at']


class DepotRole(models.Model):
    class Role(models.TextChoices):
        MANAGER = "MANAGER"
        OFFICER = "OFFICER"
        DIRECTOR = "DIRECTOR"

    depot = models.ForeignKey(
        Depot, on_delete=models.CASCADE, related_name='roles')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.OFFICER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.name}, {self.role.lower()}, {self.depot}"

    class Meta:
        unique_together = ['depot', 'user']
        ordering = ['-created_at']


class Stock(models.Model):
    depot = models.ForeignKey(
        Depot, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    stock_created = models.DateTimeField(auto_now_add=True)
    stock_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product} - {self.depot}"

    class Meta:
        ordering = ['-stock_created']
        unique_together = ['depot', 'product']


class Balance(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='balances')
    depot = models.ForeignKey(
        Depot, on_delete=models.CASCADE, related_name='balances')
    officer = models.ForeignKey(
        DepotRole,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='officers',
        limit_choices_to=Q(depot=F('depot')))
    sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_in = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.customer}-{self.depot}"

    class Meta:
        unique_together = ['depot', 'customer']
        ordering = ['-created_at']
