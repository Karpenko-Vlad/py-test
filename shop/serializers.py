from rest_framework import serializers

from .models import Product, Card, Invoice, CardItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        prod = Product.objects.create(**validated_data)
        prod.save()
        return prod


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('user_id',)

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('user_id', 'for_email', 'created_at',)
