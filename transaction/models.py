from django.db import models
from store.models import Store
from customer.models import Customer
from employee.models import Employee


class Transaction(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
