from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import InvestmentAccount, UserInvestmentAccount

class InvestmentAccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.investment_account1 = InvestmentAccount.objects.create(account_type='Investment Account 1')
        self.investment_account2 = InvestmentAccount.objects.create(account_type='Investment Account 2')
        self.investment_account3 = InvestmentAccount.objects.create(account_type='Investment Account 3')

        UserInvestmentAccount.objects.create(user=self.user, investment_account=self.investment_account1, access_level=UserInvestmentAccount.VIEW_ONLY)
        UserInvestmentAccount.objects.create(user=self.user, investment_account=self.investment_account2, access_level=UserInvestmentAccount.FULL_ACCESS)
        UserInvestmentAccount.objects.create(user=self.user, investment_account=self.investment_account3, access_level=UserInvestmentAccount.POST_ONLY)

    def test_view_only_access(self):
        url = reverse('investmentaccount-detail', args=[self.investment_account1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_access(self):
        url = reverse('investmentaccount-detail', args=[self.investment_account2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url, {'account_type': 'Updated Account'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_only_access(self):
        url = reverse('investmentaccount-detail', args=[self.investment_account3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('investmentaccount-post-transaction', args=[self.investment_account3.id])
        response = self.client.post(url, {'transaction_data': 'some_data'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)