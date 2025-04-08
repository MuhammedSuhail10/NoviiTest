from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def create_superuser(request):
    if request.data.get('username') is None or request.data.get('password') is None:
        return Response({'status':False, 'message': 'username and password are required'})
    username = request.data.get('username')
    password = request.data.get('password')
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, email=username, password=password, role='superuser')
        user.save()
        token = Token.objects.create(user=user)
        return Response({'status':True, 'token':token.key})
    return Response({'status':False, 'message': 'username already exists'})

@api_view(['POST'])
def login(request):
    if request.data.get('username') is None or request.data.get('password') is None:
        return Response({'status':False, 'message': 'Username and password are required'})
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        if not Token.objects.filter(user=user).exists():
            token = Token.objects.create(user=user)
        token = Token.objects.get(user=user)
        return Response({'status':True, 'token':token.key})
    return Response({'status':False, 'message': 'Invalid credentials'})