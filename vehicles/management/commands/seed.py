from django.core.management.base import BaseCommand
from django.db import transaction

from vehicles.models import Brand, TypeVehicle

from expenses.models import TypeExpense

class Command(BaseCommand):
    help = 'Seed the database with predefined data'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Starting the database seeding...")
        self.seed_brands()
        self.seed_type_vehicles()
        self.seed_expenses()
        self.stdout.write(self.style.SUCCESS('Successfully seeded database.'))

    def seed_brands(self):
        brands = [
            "Volkswagen", "Chevrolet", "Fiat", "Ford", "Toyota",
            "Honda", "Hyundai", "Renault", "Nissan", "Jeep",
            "Peugeot", "Citroën", "Mercedes-Benz", "BMW",
            "Audi", "Kia", "Volvo", "Mitsubishi", "Land Rover", "Jaguar"
        ]
        for brand_name in brands:
            Brand.objects.get_or_create(name=brand_name)
        self.stdout.write("Seeded brands.")

    def seed_type_vehicles(self):
        type_vehicles = [
            "Carro", "Moto", "Caminhão", "Carreta", "MotorHome"
        ]
        for type_vehicle in type_vehicles:
            TypeVehicle.objects.get_or_create(name=type_vehicle)
        self.stdout.write("Seeded vehicle types.")

    def seed_expenses(self):
        expenses = [
            "Multa", "Imposto", "Manutenção", "Abastecimento", "Revisão"
        ]
        for expense in expenses:
            TypeExpense.objects.get_or_create(name=expense)
        self.stdout.write("Seeded expenses.")
