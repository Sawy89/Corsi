from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("myview", views.my_view, name="my_view")
]
