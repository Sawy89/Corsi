from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/signup", views.signup, name="signup"),
    path("menu", views.menu, name="menu"),
    path("cart", views.shopping_cart, name="cart"),
    path("place_order", views.place_order, name="place_order"),
    path("orders", views.orders, name="orders")
]
