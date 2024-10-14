from rest_framework import serializers

from .models import Expense, TypeExpense


class TypeSerializer(serializers.ModelSerializer):
    """Serializes the Type model, including id, name, and creation timestamp."""

    class Meta:
        model = TypeExpense
        fields = ('id', 'name', 'created_at')
        
        
class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializes the Expense model, including comprehensive fields like id, name, vehicle ID, and description.
    Augments with read-only fields for vehicle and type names to provide contextual information without additional queries.
    """

    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    user = serializers.IntegerField(source='vehicle.owner.id', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
        
    class Meta:
        model = Expense
        fields = ('id', 'name', 'user', 'value', 'date', 'vehicle', 'vehicle_name', 'description', 'type', 'type_name', 'file', 'created_at')