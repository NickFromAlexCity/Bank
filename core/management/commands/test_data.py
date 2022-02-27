import password as password
from django.core.management.base import BaseCommand, CommandError
from core.models import Transactions
import random
from core.models import Currency, Category
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Creating users, permissions, currencies, categories'

    def handle(self, *args, **options):
        self._create_users()
        self._create_categories()
        self._create_currency()
        self._create_transactions()

    @staticmethod
    def _create_users():
        usernames = ["mama", "papa", "nick"]
        for name in usernames:
            u = User.objects.create(username=name)
            u.set_password(name)
            u.save()

    @staticmethod
    def _create_categories():
        names = ["Tickets", "Products", "Orderings", "Credits", "Bookings"]
        users = list(User.objects.all())

        categories = []
        for i in range(10):
            cat = Category(user=random.choice(users),
                           name=random.choice(names)
                           )
            categories.append(cat)

        Category.objects.bulk_create(categories)

    @staticmethod
    def _create_currency():
        currencies = [
            Currency(code="USD", name="United States dollar"),
            Currency(code="EUR", name="Euro"),
            Currency(code="RUB", name="Russian rouble"),
            Currency(code="DIN", name="Dinary"),
            Currency(code="YEN", name="Japan yen"),
            Currency(code="TUN", name="Mongolian tundrik"),
            Currency(code="GBP", name="British pound")
        ]
        Currency.objects.bulk_create(currencies)

    @staticmethod
    def _create_transactions():
        txs = []
        currencies = list(Currency.objects.all())
        categories = list(Category.objects.all())
        for i in range(1000):
            tx = Transactions(amount=random.randrange(Decimal(1), Decimal(1000)),
                              currency=random.choice(currencies),
                              description="",
                              date=timezone.now() - timezone.timedelta(days=random.randint(1, 356)),
                              category=random.choice(categories)
                              )
            txs.append(tx)

        Transactions.objects.bulk_create(txs)

