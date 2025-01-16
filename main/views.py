import logging

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# get the logger name 
logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    # Create landing pages views here
    return render(request, "main/index.html")



# ----------------------------- user registration and authintication ----------------------------- 

# student registration
def studentRegister(request):
    form = StudentRegistrationForm()
    
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            
            #compare the user input password and confirm password
            if password == confirm_password:
                try:
                    validate_password(password)
                    
                    if User.objects.filter(username=username).exists():
                        # messages.error(request, "Username already exists!!")
                        return redirect("studentRegister")
                
                    if User.objects.filter(email=email).exists():
                        # messages.error(request, "Email already exists!!")
                        return redirect("studentRegister")
                
                    User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    logging.basicConfig(level=logging.INFO)
                    handler = logging.FileHandler("./log/user_create.log")
                    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    logger.info(f"Create user with the username:{username} successfully.")
                                  
                    # Create a user model object for current user
                    user_model = User.objects.get(username=username)
                    student_profile = StudentProfile.objects.create(user=user_model, id_user=user_model.id)
                    student_profile.save()
                    
                    return redirect("studentLogin")
                # create a logger for the excepted error during password validation
                except ValidationError as e:
                    handler = logging.FileHandler("./log/validation_error.log")
                    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    logger.info(e)
                    
    return render(request, "./authentication/student-register.html", {"form" : form})

#login the student and redirect to main page
def studentLogin(request):
    form = StudentLoginForm()
    
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # check the existence of input username
            if not User.objects.filter(username=username).exists():
                return redirect("studentlogin")
            
            user_login = authenticate(username=username, password=password)
            
            # Login after successfully checking the user  
            if user_login is not None:
                login(request, user_login)
                return redirect("home")
    return render(request, "./authentication/student-login.html", {"form":form})

#student logout 
def studentLogout(request):
    logout(request)
    return redirect("studentLogin")
                       
#Update student profile after successfuly creating student profile
@login_required(login_url="studentLogin")
def studentProfileSetting(request, id):
    student_data = StudentProfile.objects.get(id=id)
    form = StudentProfileForm(instance=student_data)

    context ={
        "form" : form,
        "student_data" : student_data,
    }
    
    return render(request, "./authentication/student-profile-settings.html", context)
    
#Update student profile and save it to database
def updateStudentProfile(request, id):
    student_data = StudentProfile.objects.get(id=id)
    try:
        if request.method == "POST":
            form = StudentProfileForm(request.POST, request.FILES, instance=student_data)
            # Update the student profile if data is valid
            if form.is_valid():
                form.save()
                return redirect("home")
    except Exception as e:
        handler = logging.FileHandler("./log/student_profile.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(str(e))
        return redirect("home")