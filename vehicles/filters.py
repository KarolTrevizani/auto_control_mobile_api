from django_filters import rest_framework as filters


from .models import Vehicle


class VehicleFilter(filters.FilterSet):
    """
    FilterSet for the Vehicle model to enable searching and filtering via API endpoints.
    Supports filtering by vehicle name, brand, and owner. Utilized in viewsets to provide
    custom query capabilities based on user input.
    """

    class Meta:
        model= Vehicle
        fields = ['name', 'brand', 'owner']