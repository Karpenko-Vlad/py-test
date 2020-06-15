from django.urls import path
from accounts import views


urlpatterns = [
    path('registration/', views.user_registration),
]
