from rest_framework import serializers

from .models import (
    Brand, TypeVehicle, Vehicle, VehicleImage
)

from expenses.serializers import (
    ExpenseSerializer
)

class BrandSerializer(serializers.ModelSerializer):
    """Serializes Brand model data, including the identifier, name, and creation timestamp."""

    class Meta:
        model = Brand
        fields = ('id', 'name', 'created_at')
        
        
class TypeSerializer(serializers.ModelSerializer):
    """Serializes Type model data, including the identifier, name, and creation timestamp."""

    class Meta:
        model = TypeVehicle
        fields = ('id', 'name', 'created_at')


class VehicleImageSerializer(serializers.ModelSerializer):
    """Serializes VehicleImage model data, linking each image to a specific vehicle."""

    class Meta:
        model = VehicleImage
        fields = ('id', 'vehicle', 'image')

    
class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializes Vehicle model data, including comprehensive details like name, description, type, brand,
    and owner. Nested serializers include vehicle images and expenses related to the vehicle.
    Provides read-only derived fields for type name, brand name, and owner name.
    """

    type_name = serializers.CharField(source='type.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True, required=False)
    # expenses = ExpenseSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        model = Vehicle
        fields = ('id', 'name', 'owner', 'owner_name', 'description', 'type', 'type_name', 'brand', 'year', 'license_plate', 'brand_name', 'expenses', 'images', 'created_at')