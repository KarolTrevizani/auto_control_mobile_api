from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    TypeSerializer, BrandSerializer, VehicleImageSerializer, VehicleDetailsSerializer, VehicleSerializer
)

from .models import (
    Brand, TypeVehicle, Vehicle, VehicleImage
)

from .filters import (
    VehicleFilter
)


class TypeViewSet(viewsets.ModelViewSet):
    """
    Provides API actions for managing vehicle types. Supports GET, POST, PUT, and PATCH methods
    to create, read, update, and partially update vehicle types. Requires user authentication.
    """

    queryset = TypeVehicle.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']


class BrandViewSet(viewsets.ModelViewSet):
    """
    Handles API requests for vehicle brands. Allows authenticated users to perform GET, POST, PUT,
    and PATCH operations to manage brand information.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']
    

class VehicleImageViewSet(viewsets.ModelViewSet):
    """
    Manages vehicle images through API endpoints. Supports all standard model viewset actions 
    (GET, POST, DELETE, etc.) and requires user authentication to ensure data security.
    """

    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [IsAuthenticated]


class VehicleDetailViewSet(viewsets.ModelViewSet):
    """
    A comprehensive viewset managing vehicles, supporting CRUD operations and filtering capabilities.
    Authenticated users can create a vehicle and upload images simultaneously, update vehicle data,
    and replace images on update. Responses include detailed error messages or successful vehicle data.
    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetailsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = VehicleFilter
    
    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            vehicle = serializer.save()
            
            for image_file in images:
                VehicleImage.objects.create(vehicle=vehicle, image=image_file)
                
            return Response(VehicleDetailsSerializer(vehicle).data, status=status.HTTP_201_CREATED)
        else:
            return Response(f"Error: {serializer.errors}", status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()
        serializer = self.get_serializer(vehicle, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_vehicle = serializer.save()

            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                
                # Delete existing images
                vehicle.images.all().delete()
                
                # Create new images
                for image_file in images:
                    VehicleImage.objects.create(vehicle=updated_vehicle, image=image_file)

            return Response(VehicleDetailsSerializer(updated_vehicle).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = VehicleFilter

    def perform_create(self, serializer):
        """
        Assign the authenticated user's ID as the owner.
        """
        serializer.save(owner=self.request.user)