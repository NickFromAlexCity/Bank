from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Currency, Category, Transactions
from core.reports import ReportParams


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        read_only_fields = fields


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())   # protected field now: it gets self.request.user

    class Meta:
        model = Category
        fields = ("id", "name", "user")


class WriteTransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # protected field now: it gets self.request.user
    currency = serializers.SlugRelatedField(slug_field='code', queryset=Currency.objects.all())

    class Meta:
        model = Transactions
        fields = ("user", "amount", "currency", "date", "description", "category")

    def __init__(self, *args, **kwargs):
        """We need to protect field category to have its value that doesn't bellow to user made request"""
        super().__init__(*args, **kwargs)
        user = self.context["request"].user  # similar to self.request.user, but for serializer
        #self.fields["category"].queryset = Category.objects.filter(user=user)
        self.fields["category"].queryset = user.categories.all()


class ReadTransactionSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer()
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transactions
        fields = ("id", "amount", "currency", "date", "description", "category", "user",)
        read_only_fields = fields


class ReportEntrySerializer(serializers.Serializer):
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamsSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = serializers.HiddenField(  #CurrentUserDefault needs context={'request': request}
        default=serializers.CurrentUserDefault())  # protected field now: it gets self.request.user

    def create(self, validated_data):
        return ReportParams(**validated_data)