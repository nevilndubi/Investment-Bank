from rest_framework import serializers
from .models import User, InvestmentAccount, UserInvestmentAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class InvestmentAccountSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = '__all__'

class UserInvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvestmentAccount
        fields = '__all__'