from os import name
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("travel/<str:pk>", views.recommend, name="recommend"),
    path("to_recommend/<str:pk>", views.to_recommend, name="to_recommend"),
    path("search", views.search, name="search"),
]