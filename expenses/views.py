from datetime import timedelta

from django.db.models import Avg, Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import ExpenseFilter
from .models import Expense, TypeExpense
from .serializers import ExpenseSerializer, TypeSerializer


class TypeViewSet(viewsets.ModelViewSet):
    """
    Manages CRUD operations for the Type model within the API. Requires authentication for access,
    ensuring that only authenticated users can interact with type data.
    """

    queryset = TypeExpense.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticated]
    
    
class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for the Expense model, optimizing queries with `select_related` to include
    related vehicle and type data. Requires user authentication to ensure secure access to expense records.
    """

    queryset = Expense.objects.select_related('vehicle', 'type')
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter
    permission_classes = [IsAuthenticated]
    
    
class SummaryExpenseViewSet(GenericViewSet, ListModelMixin):
    """
    Provides comprehensive summaries of expenses including averages, totals, and upcoming expenses.
    This read-only viewset is accessible to all users and does not require authentication.
    Uses Django filters for filtering data based on the query parameters.
    """
    queryset = Expense.objects.select_related('vehicle', 'type').all()
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter

    def list(self, request, *args, **kwargs):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        
        today = now().date()
        six_months_ago = today - timedelta(days=180)
        
        total_last_six_months = filtered_queryset.filter(date__gte=six_months_ago).aggregate(Sum('value'))['value__sum'] or 0.00
        
        total_expenses = filtered_queryset.aggregate(Sum('value'))['value__sum'] or 0.00
        
        average_expenses_by_month = total_expenses / 12
    
        future_expenses = filtered_queryset.filter(date__gt=today).aggregate(Sum('value'))['value__sum'] or 0.00
        
        next_expense = filtered_queryset.filter(date__gt=today).order_by('date').first()
        if next_expense:
            next_expense_date = next_expense.date
        else:
            next_expense_date = "-"

        summary = {
            'average_value_of_expenses_by_month': average_expenses_by_month,
            'total_of_expense_last_six_months': total_last_six_months,
            'total_of_expenses': total_expenses,
            'date_of_the_next_expense': str(next_expense_date),
            'future_expenses': future_expenses
        }
        return Response(summary)
    

class SummaryExpenseByTypeViewSet(GenericViewSet, ListModelMixin):
    """
    Provides a summary of expenses grouped by vehicle owner and type. This read-only viewset is accessible to all users
    and does not require authentication. It uses Django filters for filtering data based on the query parameters.
    """
    queryset = Expense.objects.select_related('vehicle', 'type').all()
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter

    def list(self, request, *args, **kwargs):
        filtered_queryset = self.filter_queryset(self.get_queryset())

        summary = filtered_queryset.values('vehicle__owner__id', 'type__name').annotate(total=Sum('value')).order_by('vehicle__owner__id')
        return Response(summary)