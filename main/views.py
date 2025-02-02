import logging
import html
import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import *
from .forms import *
from .decorators import allowed_users
from .utils import fetch_categories, fetch_questions

# get the logger name 
logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    # Create landing pages views here
    return render(request, "main/index.html")

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def studentProfile(request):
    return render(request,"main/student-profile.html")


# ----------------------------- user registration and authintication ----------------------------- 
def selection(request):
    return render(request, "./authentication/selection.html")

# ---------------------- student registration and update section ----------------------
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
                    group = Group.objects.get(name="STUDENT")
                    user_model.groups.add(group)
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
                return redirect("studentProfile")
    return render(request, "./authentication/student-login.html", {"form":form})

#student logout 
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def studentLogout(request):
    logout(request)
    return redirect("studentLogin")
                       
#Update student profile after successfuly creating student profile
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def studentProfileSetting(request, id):
    student_data = StudentProfile.objects.get(user_id=id)
    form = StudentProfileForm(instance=student_data)

    context ={
        "form" : form,
        "student_data" : student_data,
    }
    
    return render(request, "./authentication/student-profile-settings.html", context)
    
#Update student profile and save it to database
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def updateStudentProfile(request, id):
    student_data = StudentProfile.objects.get(user_id=id)
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
    
#change the password for student
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def change_password_student(request):
    form = PasswordChangeForm(user=request.user)
    
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        try:   
            if form.is_valid():
                form.save()
                return redirect("studentLogin")
        except Exception as e:
            handler = logging.FileHandler("./log/password_change.log")
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.error(str(e))
            return redirect("changePasswordStudent")
            
    return render(request, "./authentication/change-password-student.html", {'form':form})
  
#add the additional student info here
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def educationLevel(request, id):
    try:
        student_data = StudentInfo.objects.get(user_id = id)
        form = StudentInfoForm(instance=student_data)
        context = {
        'form' : form,
        'student_data' : student_data
    }
    except StudentInfo.DoesNotExist:
        form = StudentInfoForm()
        context = {
            'form' : form
        }
   
    return render(request, "./authentication/update-student-edu.html", context)

#update the additional student info here
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def updateEducationLevel(request, id):
    try:
        student_data = StudentInfo.objects.get(user_id = id)
        if request.method == "POST":
            form = StudentInfoForm(request.POST, instance=student_data)
            if form.is_valid():
                form.save()
                return redirect("home")
    except StudentInfo.DoesNotExist:
        if request.method == "POST":
            form = StudentInfoForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                return redirect("home")

# ---------------------- college registration and update section ----------------------
# College registration
def collegeRegister(request):
    form = CollegeRegistrationForm()
    
    if request.method == "POST":
        form = CollegeRegistrationForm(request.POST)
        if form.is_valid():
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
                        return redirect("collegeRegister")
                
                    if User.objects.filter(email=email).exists():
                        # messages.error(request, "Email already exists!!")
                        return redirect("collegeRegister")
                
                    user = User.objects.create_user(username=username, email=email, password=password)

                    logging.basicConfig(level=logging.INFO)
                    handler = logging.FileHandler("./log/college_create.log")
                    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    logger.info(f"Create user with the username:{username} successfully.")
                                  
                    # Create a user model object for current user
                    user_model = User.objects.get(username=username)
                    group = Group.objects.get(name="COLLEGE")
                    user_model.groups.add(group)
                    college_profile = CollegeProfile.objects.create(college=user_model, id_user=user_model.id)
                    college_profile.save()
                    
                    return redirect("studentLogin")
                # create a logger for the excepted error during password validation
                except ValidationError as e:
                    handler = logging.FileHandler("./log/validation_error.log")
                    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    logger.info(e)
                    
    return render(request, "./authentication/college-registration.html", {"form" : form})

#college login
def collegeLogin(request):
    form = CollegeLoginForm()
    
    if request.method == "POST":
        form = CollegeLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # check the existence of input username
            if not User.objects.filter(username=username).exists():
                return redirect("collegelogin")
            
            user_login = authenticate(username=username, password=password)
            
            # Login after successfully checking the user  
            if user_login is not None:
                login(request, user_login)
                return redirect("home")
    return render(request, "./authentication/college-login.html", {"form":form})

#student logout 
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def collegeLogout(request):
    logout(request)
    return redirect("collegeLogin")

#Update student profile after successfuly creating student profile
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def collegeProfileSetting(request, id):
    college_data = CollegeProfile.objects.get(college_id=id)
    form = CollegeProfileForm(instance=college_data)

    context ={
        "form" : form,
        "student_data" : college_data,
    }
    
    return render(request, "./authentication/college-profile-settings.html", context)
    
#Update student profile and save it to database
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def updateCollegeProfile(request, id):
    student_data = CollegeProfile.objects.get(college_id=id)
    try:
        if request.method == "POST":
            form = CollegeProfileForm(request.POST, request.FILES, instance=student_data)
            # Update the student profile if data is valid
            if form.is_valid():
                form.save()
                return redirect("home")
    except Exception as e:
        handler = logging.FileHandler("./log/college_profile.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(str(e))
        return redirect("home")
    
#change the password for college
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def change_password_college(request):
    form = PasswordChangeForm(user=request.user)
    
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        try:   
            if form.is_valid():
                form.save()
                return redirect("collegeLogin")
        except Exception as e:
            handler = logging.FileHandler("./log/password_change.log")
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.error(str(e))
            return redirect("changePasswordCollege")
            
    return render(request, "./authentication/change-password-college.html", {'form':form})

#update college info
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def collegeInfo(request, id):
    try:
        college_data = CollegeInfo.objects.get(college_id=id)
        form = CollegeInfoForm(instance=college_data)
        context = {
            'form' : form,
            'college_data' : college_data
        }
    except CollegeInfo.DoesNotExist:
        form = CollegeInfoForm()
        context = {
            'form' : form
        }
    
    return render(request, "./authentication/update-college-info.html", context)

#update college info and save to database
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def updateCollegeInfo(request, id):
    try:
        student_data = CollegeInfo.objects.get(college_id = id)
        if request.method == "POST":
            form = CollegeInfoForm(request.POST, instance=student_data)
            if form.is_valid():
                form.save()
                return redirect("home")
    except CollegeInfo.DoesNotExist:
        if request.method == "POST":
            form = CollegeInfoForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                return redirect("home")
        
# -------------------------------------- Apptitude Test --------------------------------------
# --------------------- General Knowlwdge Test ---------------------
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def categorySelection(request):
    categories = fetch_categories()
    return render(request, "./tests/category_selection.html", {"categories": categories})


@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def aptitudeTest(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        questions = fetch_questions(category_id)
        if not questions:
            return render(request, "error.html", {"message": "Failed to fetch questions."})

        # Decode HTML entities in questions and answers
        for question in questions:
            question["question"] = html.unescape(question["question"])
            question["correct_answer"] = html.unescape(question["correct_answer"])
            question["incorrect_answers"] = [html.unescape(answer) for answer in question["incorrect_answers"]]
            # Combine correct and incorrect answers
            all_answers = question["incorrect_answers"] + [question["correct_answer"]]
            # Shuffle the answers
            random.shuffle(all_answers)
            # Store the shuffled answers in the question dictionary
            question["shuffled_answers"] = all_answers
        return render(request, "./tests/test.html", {"questions": questions})

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def testResult(request):
    total_marks = 0
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = int(key.split("_")[1])
                correct_answer = request.POST.get(f"correct_answer_{question_id}")
                if value == correct_answer:
                    total_marks += 4
                
        #Save the reult to database
        user_name = request.user
        TestResult.objects.create(user_name=user_name, total_marks=total_marks)
        return render(request, "./tests/result.html", {"total_marks" : total_marks})

# --------------------- Verbal Reasoning Test ---------------------
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def verbalReasoningTest(request):
    questions = list(Question.objects.all())
    random.shuffle(questions)
    question_list = questions[:25]
    
    request.session['quiz_questions'] = [question.id for question in question_list]
    forms = VerbalTestForm([question.id for question in question_list])
    
    return render(request, "./tests/verbal_reasoning.html", {"forms" : forms})

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def verbalTestCheck(request):
    if request.method == "POST":
        question_ids = request.session.get('quiz_questions', [])
        form = VerbalTestForm(question_ids, request.POST)
        if form.is_valid():
            total_marks = 0
            for kay, value in form.cleaned_data.items():
                selected_option = Options.objects.get(id=value)
                if selected_option.is_true:
                    total_marks += 4
        #Save the reult to database
        user_name = request.user
        TestResult.objects.create(user_name=user_name, total_marks=total_marks)
        return render(request, "./tests/result.html", {"total_marks" : total_marks})       
            
def result_view(request):
    results = TestResult.objects.all().order_by("-date")
    return render(request, "results.html", {"results": results})
 