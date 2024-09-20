import json
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import InvestmentAccount, UserInvestmentAccount, Transaction
from api.serializer import UserSerializer, InvestmentAccountSerializer, TransactionSerializer

class InvestmentAccountAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.user3 = User.objects.create_user(username='user3', password='password123')
        
        self.account1 = InvestmentAccount.objects.create(account_type='Investment Account 1', account_number='INV001')
        self.account2 = InvestmentAccount.objects.create(account_type='Investment Account 2', account_number='INV002')
        self.account3 = InvestmentAccount.objects.create(account_type='Investment Account 3', account_number='INV003')
        
        UserInvestmentAccount.objects.create(user=self.user1, investment_account=self.account1, access_level='view')
        UserInvestmentAccount.objects.create(user=self.user1, investment_account=self.account2, access_level='full')
        UserInvestmentAccount.objects.create(user=self.user1, investment_account=self.account3, access_level='post')
        
        UserInvestmentAccount.objects.create(user=self.user2, investment_account=self.account1, access_level='full')
        UserInvestmentAccount.objects.create(user=self.user2, investment_account=self.account2, access_level='post')
        
        UserInvestmentAccount.objects.create(user=self.user3, investment_account=self.account3, access_level='view')
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        
        # Create some transactions
        Transaction.objects.create(transaction_type='deposit', amount=1000, account=self.account1, created_at=datetime.now() - timedelta(days=1))
        Transaction.objects.create(transaction_type='withdrawal', amount=500, account=self.account1, created_at=datetime.now() - timedelta(days=2))
        Transaction.objects.create(transaction_type='deposit', amount=2000, account=self.account2, created_at=datetime.now() - timedelta(days=3))
        Transaction.objects.create(transaction_type='transfer', amount=1000, account=self.account3, created_at=datetime.now() - timedelta(days=4))

    def test_user_permissions(self):
        # Test view-only access
        response = self.client.get(reverse('investment-account-detail', kwargs={'pk': self.account1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.post(reverse('investment-account-detail', kwargs={'pk': self.account1.id}), data={'account_type': 'Investment Account 1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test full access
        response = self.client.get(reverse('investment-account-detail', kwargs={'pk': self.account2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.post(reverse('investment-account-detail', kwargs={'pk': self.account2.id}), data={'account_type': 'Investment Account 2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test post-only access
        response = self.client.get(reverse('investment-account-detail', kwargs={'pk': self.account3.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.post(reverse('investment-account-detail', kwargs={'pk': self.account3.id}), data={'account_type': 'Investment Account 3'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_endpoint(self):
        # Test without date range
        response = self.client.get(reverse('user-transactions', kwargs={'user_id': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertIn('total_balance', response.data)
        
        # Test with date range
        start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        response = self.client.get(reverse('user-transactions', kwargs={'user_id': self.user1.id}), {'start_date': start_date, 'end_date': end_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertIn('total_balance', response.data)

    def test_multiple_users_per_account(self):
        # Test that multiple users can be associated with an account
        response = self.client.get(reverse('user-investment-account-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)

    def test_user_multiple_accounts(self):
        # Test that a user can have multiple accounts
        response = self.client.get(reverse('user-investment-account-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user1_accounts = [item for item in response.data if item['user'] == self.user1.id]
        self.assertEqual(len(user1_accounts), 3)

    def test_transaction_creation(self):
        # Test creating a transaction
        data = {
            'transaction_type': 'deposit',
            'amount': 500,
            'account': self.account2.id
        }
        response = self.client.post(reverse('transaction-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('transaction_type', response.data)
        self.assertIn('amount', response.data)
        self.assertIn('account', response.data)

    def test_transaction_list(self):
        # Test listing transactions
        response = self.client.get(reverse('transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
       