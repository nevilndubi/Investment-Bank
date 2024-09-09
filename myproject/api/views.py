from django.shortcuts import render

# My views are here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

@api_view(['GET'])
def get_user(request):
    return Response(UserSerializer({'name': 'John', 'email': 'john@example.com'}))