from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("results", views.search, name="search"),
    path("newentry", views.newentry, name="newentry")
]
