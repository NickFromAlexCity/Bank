from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions') # if the user is deleted all the its transactions going to be deleted too.
    # user.transactions.all()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='transactions')
    date = models.DateField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')

    def __str__(self):
        return f"{self.amount} {self.currency.code} {self.date}"


class AllowList(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address