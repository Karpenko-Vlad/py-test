from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from shop import views as shop_views
from accounts import views as account_views

router = routers.DefaultRouter()
router.register(r'cards', shop_views.CardViewSet)
router.register(r'products', shop_views.ProductViewSet)
router.register(r'invoices', shop_views.InvoiceViewSet)

router.register(r'users', account_views.UserViewSet)

urlpatterns = [
    path('auth/registration/', include('accounts.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('shop/', include('shop.urls')),

    path('admin/api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
