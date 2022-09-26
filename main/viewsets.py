import re
from .models import User
from rest_framework import viewsets, response, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True, url_path='login', url_name='login')
    def login(self, request, *args, **kwargs):
        
        email = request.query_params.get('email');
        password = request.query_params.get('password');
        queryset = User.objects.filter(email=email,password=password).values();
        return Response(queryset);
