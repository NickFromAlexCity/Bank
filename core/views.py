from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_xml.renderers import XMLRenderer

from core.models import Currency, Category, Transactions
from core.permissions import IsAdminOrReadOnly, AllowListPermission
from core.reports import transaction_report
from core.serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, \
    ReadTransactionSerializer, ReportEntrySerializer, ReportParamsSerializer


class CurrencyModelViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None
    renderer_classes = [JSONRenderer, XMLRenderer, ]


class CategoryModelViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions | AllowListPermission]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionsModelViewSet(ModelViewSet): 
    queryset = Transactions.objects.select_related("currency", "category", "user")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("description",)
    ordering_fields = ("amount", "date")
    filterset_fields = ("currency__code",)

    def get_queryset(self):
        """
        This queryset allows the application to be used by several users. Each user will have itself transactions.
        """
        return Transactions.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)
    # Instead if this I change user field in WriteTransactionSerializer


class TransactionReportAPIView(APIView):
    def get(self, request):
        params_serializer = ReportParamsSerializer(data=request.GET,
                                                   context={'request': request}) # It is because we use CurrentUserDefault in serializer

        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()
        data = transaction_report(params)
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(serializer.data)
