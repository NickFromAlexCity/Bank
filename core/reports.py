import datetime
from dataclasses import dataclass
from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg

from core.models import Transactions, Category


@dataclass
class ReportEntry:
    category: Category
    total: Decimal
    count: int
    avg: Decimal


@dataclass
class ReportParams:
    start_date: datetime.datetime
    end_date: datetime.datetime
    user: User


def transaction_report(params: ReportParams):
    data = []

    # Group by 'category'
    queryset = Transactions.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date__lte=params.end_date,
    ).values("category").annotate(
        total=Sum("amount"),
        count=Count("id"),
        avg=Avg("amount")
    )

    category_index = {}
    for category in Category.objects.filter(user=params.user):
        category_index[category.pk] = category

    for entry in queryset:
        #category = Category.objects.get(pk=entry["category"])
        category = category_index.get(entry["category"])
        report_entry = ReportEntry(category, entry["total"], entry["count"], entry["avg"])
        data.append(report_entry)

    return data
