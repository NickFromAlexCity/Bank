from django.core.management.base import BaseCommand, CommandError
from core.models import Transactions
import random
from core.models import Currency, Category
from decimal import Decimal
from django.utils import timezone


# Todo: add Currency and Category objects firstly,
#  create users with different rights
#  define specific permissions for specific user
class Command(BaseCommand):
    help = 'Fill-full the database'

    def handle(self, *args, **options):
        txs = []
        currencies = list(Currency.objects.all())
        categories = list(Category.objects.all())
        for i in range(1000):
            tx = Transactions(amount=random.randrange(Decimal(1), Decimal(1000)),
                              currency=random.choice(currencies),
                              description="",
                              date=timezone.now()-timezone.timedelta(days=random.randint(1, 356)),
                              category=random.choice(categories)
                              )
            txs.append(tx)

        Transactions.objects.bulk_create(txs)
        print("Transactions count:", Transactions.objects.count())
