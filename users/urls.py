from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("success/", views.success, name="success"),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/<int:pk>/follow/', views.follow_user, name='follow_user'),
    path('profile/<int:pk>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path("debug/user_ids/", views.user_ids_debug, name="user_ids_debug"),  # Debug route to see all user
    path("search/", views.user_search, name="user_search"),
]