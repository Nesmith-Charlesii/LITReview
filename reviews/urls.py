from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
    path("<int:pk>/", views.book_detail, name="book_view"),
    path('reviews/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),

    path('add_book/', views.add_book, name='add_book')
]