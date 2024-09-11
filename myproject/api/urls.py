from django.urls import path
from .views import get_users, create_user, user_detail, investment_accounts, investment_account_detail, register_user
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('users/', get_users, name='get_users'),
    path('users/create', create_user, name='create_user'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('accounts/', investment_accounts, name='investment_accounts'),
    path('accounts/<int:pk>/', investment_account_detail, name='investment_account_detail'),
    path('register/', views.register_user, name='register'),
]