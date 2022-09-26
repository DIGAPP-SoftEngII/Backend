from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('<int:user_id>/account/', views.user_profile, name='user_profile'),
    path('login/', views.login_request, name='login'),
    path('<int:business_id>/biz_profile', views.business_profile, name='biz_profile'),
    path('cities/', views.cities, name='cities'), # test
]