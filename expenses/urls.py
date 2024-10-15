from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ExpenseViewSet, SummaryExpenseByTypeViewSet,
                    SummaryExpenseViewSet, TypeViewSet)

app_name = 'expenses'

router = DefaultRouter()

router.register(r'expenses', ExpenseViewSet)
router.register(r'type-expenses', TypeViewSet)
router.register(r'summary-by-type', SummaryExpenseByTypeViewSet)
router.register(r'summary', SummaryExpenseViewSet)


urlpatterns = router.urls
