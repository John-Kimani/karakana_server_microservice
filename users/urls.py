from django.urls import path
from . import views


urlpatterns = [

    path('', views.product_list, name='Products'),
    path('cart/', views.add_to_cart, name='Cart'),
    path('checkout/', views.checkout, name='Checkout')
]