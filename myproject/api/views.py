from django.shortcuts import render, redirect

# My views are here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, InvestmentAccount, UserInvestmentAccount
from .serializer import UserSerializer, InvestmentAccountSerializer, UserInvestmentAccountSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    # Checking to see if the user is logging in
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'Invalid login credentials, Try Again')
            return redirect('home')
    else:    
         return render(request, 'home.html', {})

def logout_user (request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'You have successfully registered')
            return redirect('home')
        else:
            messages.error(request, 'Error registering user')
            return redirect('home')
    return render(request, 'register.html', {})

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

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)