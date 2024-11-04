from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from expenses.models import TypeExpense
from expenses.serializers import TypeSerializer


class TypeViewSetTest(APITestCase):

    def setUp(self):
        # Configura um tipo de despesa para testes de listagem
        self.type_expense = TypeExpense.objects.create(name="Fuel")
        self.url_list = reverse('expenses:type-expenses-list')

    def test_get_type_expense_list(self):
        """Testa a lista de tipos de despesas"""
        response = self.client.get(self.url_list)
        types = TypeExpense.objects.all()
        serializer = TypeSerializer(types, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_type_expense(self):
        """Testa a criação de um novo tipo de despesa"""
        data = {"name": "Maintenance"}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TypeExpense.objects.count(), 2)
        self.assertEqual(TypeExpense.objects.get(id=response.data['id']).name, "Maintenance")
