from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from expenses.models.py import Expense, Vehicle, TypeExpense
from expenses.serializers import ExpenseSerializer
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class ExpenseViewSetTest(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password', email='test@example.com', cnh='123456')
        self.client.force_authenticate(user=self.user)
        
        # Create a vehicle and a type of expense for testing
        self.vehicle = Vehicle.objects.create(name="Car")
        self.type_expense = TypeExpense.objects.create(name="Fuel")
        
        # Create an expense for testing
        self.expense = Expense.objects.create(
            name="Gasoline",
            vehicle=self.vehicle,
            description="Fuel expense",
            type=self.type_expense,
            value=50.00,
            date=datetime.date.today()
        )
        
        self.url_list = reverse('expenses:expenses-list')
        self.url_detail = reverse('expenses:expenses-detail', args=[self.expense.id])

    def test_get_expense_list(self):
        """Test the list of expenses"""
        response = self.client.get(self.url_list)
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_expense(self):
        """Test the creation of a new expense"""
        data = {
            "name": "Maintenance",
            "vehicle": self.vehicle.id,
            "description": "Vehicle maintenance",
            "type": self.type_expense.id,
            "value": 200.00,
            "date": datetime.date.today()
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual(Expense.objects.get(id=response.data['id']).name, "Maintenance")

    def test_update_expense(self):
        """Test the update of an existing expense"""
        data = {
            "name": "Updated Gasoline",
            "vehicle": self.vehicle.id,
            "description": "Updated description",
            "type": self.type_expense.id,
            "value": 60.00,
            "date": datetime.date.today()
        }
        response = self.client.put(self.url_detail, data)
        self.expense.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.expense.name, "Updated Gasoline")
        self.assertEqual(self.expense.value, 60.00)

    def test_delete_expense(self):
        """Test the deletion of an expense"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)
