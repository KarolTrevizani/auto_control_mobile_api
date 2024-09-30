from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Vehicle, Brand, TypeVehicle, User

from .serializers import VehicleSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


class BrandModelTests(TestCase):
    def test_string_representation(self):
        brand = Brand(name='Toyota')
        self.assertEqual(str(brand), 'Toyota')

    def test_default_creation_date(self):
        brand = Brand(name='Toyota')
        brand.save()
        self.assertIsNotNone(brand.created_at)


class VehicleSerializerTests(APITestCase):
    def test_vehicle_serialization(self):
        user = User.objects.create(username='testuser')
        brand = Brand.objects.create(name='Toyota')
        type_vehicle = TypeVehicle.objects.create(name='Sedan')
        vehicle = Vehicle.objects.create(
            name='Camry', description='Reliable car', type=type_vehicle,
            brand=brand, owner=user, year=2020, license_plate='ABC123'
        )
        serializer = VehicleSerializer(vehicle)
        self.assertEqual(serializer.data['name'], 'Camry')
        self.assertEqual(serializer.data['type_name'], 'Sedan')
        self.assertEqual(serializer.data['brand_name'], 'Toyota')
        self.assertEqual(serializer.data['owner_name'], user.username)

class VehicleViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='user_test@gmail.com', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        self.brand = Brand.objects.create(name='Toyota')
        self.type_vehicle = TypeVehicle.objects.create(name='Sedan')
        self.vehicle_data = {
            'name': 'Camry',
            'description': 'Reliable car',
            'type': self.type_vehicle.id,
            'brand': self.brand.id,
            'owner': self.user.id,
            'year': 2020,
            'license_plate': 'ABC123'
        }
        self.create_url = reverse('vehicles:vehicle-list')

    def test_create_vehicle(self):
        response = self.client.post(self.create_url, self.vehicle_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)

    def test_update_vehicle(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        update_url = reverse('vehicles:vehicle-detail', args=[vehicle.id])
        update_data = {'description': 'Very reliable car'}
        response = self.client.patch(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.description, 'Very reliable car')

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
