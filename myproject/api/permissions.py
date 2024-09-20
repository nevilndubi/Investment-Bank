from rest_framework.permissions import BasePermission
from .models import UserInvestmentAccount

class IsViewOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_investment_account = UserInvestmentAccount.objects.get(user=request.user, investment_account=obj)
            return user_investment_account.access_level == UserInvestmentAccount.VIEW_ONLY
        except UserInvestmentAccount.DoesNotExist:
            return False

class IsFullAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_investment_account = UserInvestmentAccount.objects.get(user=request.user, investment_account=obj)
            return user_investment_account.access_level == UserInvestmentAccount.FULL_ACCESS
        except UserInvestmentAccount.DoesNotExist:
            return False

class IsPostOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_investment_account = UserInvestmentAccount.objects.get(user=request.user, investment_account=obj)
            return user_investment_account.access_level == UserInvestmentAccount.POST_ONLY
        except UserInvestmentAccount.DoesNotExist:
            return False