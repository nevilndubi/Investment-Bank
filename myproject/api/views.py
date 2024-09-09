from django.shortcuts import render

# My views are here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

@api_view(['GET'])
def get_user(request):
    try:
        # Create a new User object with the given details
        user = User.objects.create(name='John', email='john@example.com', age=30)
        
        # Serialize the created User object
        serialized_user = UserSerializer(user).data
        
        return Response(serialized_user, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)