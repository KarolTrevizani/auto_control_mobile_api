import datetime

from django.db import models
from django.utils import timezone

from vehicles.models import (
    Vehicle
)

class TypeExpense(models.Model):
    """Represents a categorization type with name and creation date."""

    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Type: {self.name}"


class Expense(models.Model):
    """
    Records an expense linked to a vehicle, categorized by type, with optional file attachment. 
    Tracks the creation date.
    """

    name = models.CharField(max_length=255)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="expenses")
    description = models.TextField(max_length=500, default="")
    type = models.ForeignKey(TypeExpense, on_delete=models.SET_NULL, null=True)
    file = models.FileField(null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Type: {self.name}"

