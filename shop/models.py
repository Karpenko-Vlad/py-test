import os

from django.db import models
from rest_framework import permissions

from accounts.models import User


class AdminAccessPermission(permissions.BasePermission):
    message = 'Check admin permission.'

    def has_permission(self, request, view):
        return request.user.is_superuser


class Product(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to="media/images/", null=True)

    price = models.FloatField()


class Card(models.Model):
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    user = models.ForeignKey(User, related_name="cards", on_delete=models.CASCADE)


class CardItem(models.Model):
    def __str__(self):
        return self.item.name

    card = models.ForeignKey(Card, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class Invoice(models.Model):
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    user = models.ForeignKey(User, related_name="invoices", on_delete=models.CASCADE)
    for_email = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    fixed_price = models.CharField(max_length=30)
    count = models.IntegerField(default=1)
