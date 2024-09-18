from django.db import models
from django.utils import timezone

from users.models import User

app_name = "vehicles"


class Brand(models.Model):
    """Represents a vehicle brand with its name and the date it was created."""

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    

class TypeVehicle(models.Model):
    """Defines a vehicle type with its name and the date it was created."""

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    
class Vehicle(models.Model):
    """
    Details a vehicle, linking it to a specific type, brand, and owner. Includes optional description and
    creation date. The model provides a concise representation that simply returns the vehicle's name.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    type = models.ForeignKey(TypeVehicle, null=True, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)
    license_plate = models.CharField(max_length=50, default="")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} {self.license_plate}"
    

class VehicleImage(models.Model):
    """Associates images with vehicles, storing each image under 'images_vehicles/' directory."""

    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images_vehicles/')
    