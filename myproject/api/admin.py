from django.contrib import admin
from .models import User, Bank, Branch, InvestmentAccount

# Register your models here.
admin.site.register(User)
admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(InvestmentAccount)