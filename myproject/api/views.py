from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import Http404

# My views are here.
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User, InvestmentAccount, UserInvestmentAccount, Bank, Branch, Transfer, Withdraw, Deposit, Transaction
from .models import *
from .serializer import *
from .permissions import IsViewOnly, IsFullAccess, IsPostOnly
from .serializer import UserSerializer, InvestmentAccountSerializer, UserInvestmentAccountSerializer, UserRegistrationSerializer, BankSerializer, BranchSerializer, TransferSerializer, WithdrawSerializer, DepositSerializer, TransactionSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.db.models import Sum
from datetime import datetime
from .serializer import UserRegistrationSerializer

class BanksAPIView(generics.ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class BankDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class BranchesAPIView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class BranchDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        account = serializer.save()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsViewOnly]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsFullAccess]
        elif self.action == 'post_transaction':
            self.permission_classes = [IsAuthenticated, IsPostOnly]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def post_transaction(self, request, pk=None):
        # Implement the logic for posting a transaction
        pass

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        transaction = serializer.save()
        account = transaction.account
        if transaction.transaction_type == 'withdraw':
            account.balance -= transaction.amount
        elif transaction.transaction_type == 'deposit':
            account.balance += transaction.amount
        elif transaction.transaction_type == 'transfer':
            account.balance -= transaction.amount
            recipient_account = Transfer.objects.get(transaction=transaction).recipient_account
            recipient_account.balance += transaction.amount
            recipient_account.save()
        account.save()

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated, IsFullAccess]

class WithdrawViewSet(viewsets.ModelViewSet):
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated, IsFullAccess]

class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated, IsFullAccess]

def home(request):
    users = User.objects.all()
    # Checking to see if the user is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'Invalid login credentials, Try Again')
            return redirect('home')
    else:    
         return render(request, 'home.html', {'users': users})

def logout_user (request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully been registered')
            return redirect('home')
    else:   
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
       serializer.save() 
       return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def investment_accounts(request):
    if request.method == 'GET':
        accounts = InvestmentAccount.objects.all()
        serializer = InvestmentAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InvestmentAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def investment_account_detail(request, pk):
    try:
        account = InvestmentAccount.objects.get(pk=pk)
    except InvestmentAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvestmentAccountSerializer(account)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InvestmentAccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def user_transactions(request, user_id):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        transactions = Transaction.objects.filter(account__users__id=user_id, created_at__range=[start_date, end_date])
    else:
        transactions = Transaction.objects.filter(account__users__id=user_id)

    total_balance = InvestmentAccount.objects.filter(users__id=user_id).aggregate(Sum('balance'))['balance__sum']
    serializer = TransactionSerializer(transactions, many=True)

    return Response({
        'transactions': serializer.data,
        'total_balance': total_balance
    }, status=status.HTTP_200_OK)