from django_filters import rest_framework as filters

from .models import Expense


class ExpenseFilter(filters.FilterSet):
    """Provides filtering capabilities to filter by vehicle owner id and vehicle id."""
        
    user = filters.NumberFilter(field_name='vehicle__owner__id')
    vehicle = filters.NumberFilter(field_name='vehicle__id')
    
    class Meta:
        model = Expense
        fields = ('user', 'vehicle')
