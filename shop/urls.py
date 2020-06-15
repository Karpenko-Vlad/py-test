from django.urls import path

from shop import views

urlpatterns = [
    path('products/', views.products),
    path('card/item/', views.product_add_to_card),
    path('card/buy/', views.card_buy),
]
