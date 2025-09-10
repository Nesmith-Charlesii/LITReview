from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
    path("books/<int:pk>/", views.book_detail, name="book_view"),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
]