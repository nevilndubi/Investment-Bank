from django.contrib import admin
from .models import User, Bank, Branch, InvestmentAccount, UserInvestmentAccount, Transfer, Withdraw, Deposit, Transaction

# Register your models here.
admin.site.register(User)
admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(InvestmentAccount)
admin.site.register(UserInvestmentAccount)
admin.site.register(Transfer)
admin.site.register(Withdraw)
admin.site.register(Deposit)
admin.site.register(Transaction)