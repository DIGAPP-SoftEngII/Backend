import re
from .models import User, Business
from rest_framework import viewsets, response, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import BusinessSerializer, UserSerializer 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True, url_path='login', url_name='login')
    def login(self, request, *args, **kwargs):
        
        email = request.query_params.get('email');
        password = request.query_params.get('password');
        queryset = User.objects.filter(email=email,password=password).values();
        return Response(queryset);

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    @action(methods=['get'], detail=True, url_path='login', url_name='loginBusiness')
    def loginBusiness(self, request, *args, **kwargs):
        
        name = request.query_params.get('name');
        #password = request.query_params.get('password');
        queryset = Business.objects.filter(name=name).values();
        return Response(queryset)

    # def create(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # user = serializer.save()
    #     return []
    #     print('***************')
    #     print(request.data)
    #     print('***************')
    #     user.set_password(serializer.validated_data.get('password'))
    #     user.save()
    #     headers = self.get_success_headers(serializer.data)

    #     return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
