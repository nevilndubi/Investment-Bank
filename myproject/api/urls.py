from django.urls import path, re_path
from .views import get_users, create_user, user_detail, investment_accounts, investment_account_detail, register_user, BanksAPIView, BranchesAPIView, BranchDetailAPIView, BankDetailAPIView, InvestmentAccountViewSet, TransferViewSet, WithdrawViewSet, DepositViewSet
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
    path('investment-accounts/', InvestmentAccountViewSet.as_view({'get': 'list', 'post': 'create'}), name='investment-accounts'),
    path('investment-accounts/<int:pk>/', InvestmentAccountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='investment-account-detail'),
    path('transfers/', TransferViewSet.as_view({'get': 'list', 'post': 'create'}), name='transfers'),
    path('transfers/<int:pk>/', TransferViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='transfer-detail'),
    path('withdraws/', WithdrawViewSet.as_view({'get': 'list', 'post': 'create'}), name='withdraws'),
    path('withdraws/<int:pk>/', WithdrawViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='withdraw-detail'),
    path('deposits/', DepositViewSet.as_view({'get': 'list', 'post': 'create'}), name='deposits'),
    path('deposits/<int:pk>/', DepositViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='deposit-detail'),
    re_path(r'^banks', BanksAPIView.as_view(), name='banks'),
    re_path(r'^bank/(?P<pk>[0-9]+)/', BankDetailAPIView.as_view(), name='bank-detail'),
    re_path(r'^branches/', BranchesAPIView.as_view(),name='branches'),
    re_path(r'^branch/(?P<pk>[0-9]+)/', BranchDetailAPIView.as_view(),name='branch-detail'),
]