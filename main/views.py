import logging

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

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
def student_register(request):
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
                        return redirect("home")
                
                    if User.objects.filter(email=email).exists():
                    # messages.error(request, "Email already exists!!")
                        return redirect("home")
                
                    User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    logging.basicConfig(level=logging.INFO)
                    handler = logging.FileHandler("./log/user_create.log")
                    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    logger.info(f"Create user with the username:{username} successfully.")
                    
                    # Log user in and redirect to user profile creation page
                    user_login = authenticate(username=username, password=password)
                    login(request, user_login)
                    
                    
                    # Create a user model object for current user
                    user_model = User.objects.get(username=username)
                    user_login = StudentProfile.objects.create(user=user_model, id_user=user_model.id)
                    user_login.save()
                    
                    return redirect("home")
                
                except ValidationError as e:
                    pass
    return render(request, "./authentication/student-register.html", {"form" : form})