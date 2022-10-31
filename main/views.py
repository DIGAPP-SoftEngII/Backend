from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from .models import *
from .forms import NewUserForm
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action    
from .serializers import *
from .forms import NewUserForm, ReportForm
from django.contrib.auth import get_user_model
from django.db.models import Avg


User = get_user_model()

# API

class BusinessView(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
        
    
class CityView(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()

class ConsultView(viewsets.ModelViewSet):
    serializer_class = ConsultSerializer
    queryset = Consult.objects.all()

class FavoriteView(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

class ReportView(APIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Report with given todo data
        '''
        data = {
            'id' : request.data.get('id'),
            'date' : request.data.get('date'),
            'internet_status': request.data.get('internet_status'), 
            'rating_business': request.data.get('rating_business'), 
            'report_support' : request.data.get('report_support'),
            'comments' : request.data.get('comments'),
            'user_id': request.data.get('user_id'),
            'business_id': request.data.get('business_id'),
            'occupation_status': request.data.get('occupation_status')
        }
        
        # We modify now every time 
        business_id = request.data.get('business_id')
        business = get_object_or_404(Business, pk=business_id)
        
        business.rating= round(Report.objects.filter( business_id__exact=business_id).aggregate(Avg('rating_business') )['rating_business__avg'], 1) # Round to 1 digit
        business.internet_quality= round( Report.objects.filter(business_id__exact=business_id).aggregate(Avg('internet_status'))['internet_status__avg'], 1) # Round to one digit
        business.save()
        
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReportViewDetail(APIView):
    def get_object(self, report_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, report_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        report_instance = self.get_object(report_id)
        if not report_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReportSerializer(report_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, report_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        report_instance = self.get_object(report_id)
        if not report_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'internet_status': request.data.get('internet_status'), 
            'rating_business': request.data.get('rating_business'), 
            'comments': request.data.get('comments'), 
        }
        serializer = ReportSerializer(instance = report_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, report_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        report_instance = self.get_object(report_id)
        if not report_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        report_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

#######################################################################################
"""TEMPLATES DJANGO, Just for testing"""

def login_user(request):
    email = request.GET['email']
    password = request.GET['username']

    user = User.objects.get(email=email)

# Create your views here.
def homepage(request):
    return render(request=request, 
                  template_name='main/index.html',
                  context={ "businesses": Business.objects.all })


# USER VIEWS
def register(request):
    if request.method == "POST":
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                            template_name = "main/register.html",
                            context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect("main:homepage")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f'Your logged in as {username}')
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, 
                 "main/login.html", 
                 {"form": form})


def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    reports = list( user.report_set.all() )
    number_reports = len(reports)
    #return HttpResponse("Currently you are in  <strong>A USER PROFILE ! ! !</strong>")
    return render(request, "main/user_profile.html", {
        "user" : user,
        "number_reports": number_reports
    })

# BUSINESS VIEWS
def business_profile(request, business_id):
    business = get_object_or_404(Business, pk=business_id)
    
    #return HttpResponse("Currently you are in  <strong>A BUSINESS</strong>")
    return render(request, "main/biz_detail.html", {
        "business" : business
    })

def support_report(request, business_id):
    business = get_object_or_404(Business, pk=business_id) # Question.objects.get(pk=1) # Handle error for selected question
    
    try: # handle error for selected choice
        selected_report = business.report_set.get(pk=request.POST["button_support"]) # Rescata la opción que está en "value" del HTML llamado "button_support" que es el id del objeto de tipo 'Report'.
        # En el form la clave es: name='button_support' value={{report.id}}
    except(KeyError, Report.DoesNotExist):
        return render(request, "main/biz_profile.html", {
            "business": business,
            "error_message": "No elegiste un reporte"
        })
    else:
        selected_report.report_support += 1
        selected_report.save()
        return HttpResponseRedirect( reverse("main:biz_profile", args=(business.id, ) ) )

def make_report(request, business_id):
    if request.method == "POST":
        form = ReportForm(data=request.POST)
        if form.is_valid():
            form.save()
            business = get_object_or_404(Business, pk=business_id)
            business.rating= round(Report.objects.filter(business_id__exact=business_id).aggregate(Avg('rating_business'))['rating_business__avg'],1)
            business.internet_quality= round(Report.objects.filter(business_id__exact=business_id).aggregate(Avg('internet_status'))['internet_status__avg'],1)
            business.save()
            return HttpResponseRedirect( reverse("main:biz_profile", args=(business_id, ) ) ) # Templates Django
        else:
            messages.error(request, "Invalid form!")


    form = ReportForm()
    return render(request, "main/make_report.html", {
        "form": form,
        })
    
       
# def add_favorite(request, business_id):
#     business = get_object_or_404(Business, pk=business_id) # Question.objects.get(pk=1) # Handle error for selected question
    
#     try: # handle error for selected choice
#         selected_report = business.report_set.get(pk=request.POST["button_support"]) # Rescata la opción que está en "value" del HTML llamado "choice" que es el id del objeto de tipo 'Choice'.
#         # En el form la clave es: name='button_support' value={{report.id}}
#     except(KeyError, Report.DoesNotExist):
#         return render(request, "main/biz_profile.html", {
#             "business": business,
#             "error_message": "No elegiste un reporte"
#         })
#     else:
#         selected_report.report_support += 1
#         selected_report.save()
#         return HttpResponseRedirect( reverse("main:biz_profile", args=(business.id, ) ) )


def cities(request):
    return HttpResponse("HEY TODAY IS OCTOBER  31st. Currently you are in  <strong>CITY</strong>, to change click the button below.")