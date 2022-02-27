from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from core import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register("categories", views.CategoryModelViewSet, basename="category")
router.register("transactions", views.TransactionsModelViewSet, basename="category")
router.register("currencies", views.CurrencyModelViewSet, basename="currency")
urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("login/", obtain_auth_token, name="obtain-auth-token"),
    path("report/", views.TransactionReportAPIView.as_view(), name="transaction_report")
] + router.urls
