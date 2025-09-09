from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
    path("books/<int:pk>/", views.book_detail, name="book_view"),
]