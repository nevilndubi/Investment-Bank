from rest_framework import serializers
from .models import User, InvestmentAccount, UserInvestmentAccount, Bank, Branch
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            password=make_password(validated_data['password']),
        )
        user.save()
        return user
    
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('__all__')

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')

class InvestmentAccountSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = '__all__'

class UserInvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvestmentAccount
        fields = '__all__'