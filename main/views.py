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
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib import messages

from .models import *
from .forms import *
from .decorators import allowed_users
from .utils import fetch_categories, fetch_questions

# get the logger name 
logger = logging.getLogger(__name__)

def home(request):
    # gallery = Gallery.objects.all()
    # faqs = Faqs.objects.all()
    testimonila = Testimonial.objects.all()
    news = New.objects.filter(is_approved=True).order_by('date')[ :2]
    event_cat = EventCategory.objects.all()
  
    cate_id = request.GET.get('cat_id')
    if cate_id:
        events = Event.objects.filter(id=cate_id, is_approved=True)
    else:
        events = Event.objects.filter(is_approved=True)
    
    context = {
        # "gallery" : gallery,
        # "question" : faqs,
        "testimonials" : testimonila,
        "news" : news,
        "events" : events,
        "cat" : event_cat,
    }
    return render(request, "main/index.html", context)

def collegeAbroad(request):
    return render(request, "main/404.html")

def collegeNepal(request):
    college_location = request.GET.get("location")
    if college_location:
        college_data = CollegeProfile.objects.filter(college_location_id = college_location)
    else:
        college_data = CollegeProfile.objects.all()
    location = CollegeLocation.objects.all()
    
    paginator = Paginator(college_data, 6)
    page_num = request.GET.get('page')
    data = paginator.get_page(page_num)
    total_page = data.paginator.num_pages
     
    context = {
        "college_data" : data,
        "num" : [n+1 for n in range(total_page)],
        "location" : location
    }
    
    return render(request, "main/colleges_in_Nepal.html", context)

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def studentProfile(request, id):
    data = StudentProfile.objects.get(user_id=id)
    return render(request,"main/student-profile.html",{"data":data})

@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def collegeProfile(request, id):
    data = CollegeProfile.objects.get(id_user=id)
    course = CollegeInfo.objects.filter(college_name_id = id)
    application = Application.objects.filter(college_name = id)
    
    context = {
        "data" : data,
        "course" : course,
        "application" : application
    }
    return render(request,"main/college_profile.html", context)

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
            
            if password == confirm_password:
                try:
                    validate_password(password)
                    
                    if User.objects.filter(username=username).exists():
                        messages.error(request, "Username already exists!!")
                        return redirect("studentRegister")
                
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "Email already exists!!")
                        return redirect("studentRegister")
                
                    User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    messages.success(request,"Your account has been successfully created!")
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

def studentLogin(request):
    form = StudentLoginForm()
    
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # check the existence of input username
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username or password doen't match!!")
                return redirect("studentlogin")
            
            user_login = authenticate(username=username, password=password)
            
            # Login after successfully checking the user  
            if user_login is not None:
                login(request, user_login)
                return redirect("home")
    return render(request, "./authentication/student-login.html", {"form":form})
 
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def studentLogout(request):
    logout(request)
    return redirect("studentLogin")
                       
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def studentProfileSetting(request):
    id = request.user.id
    student_data = StudentProfile.objects.get(user_id=id)
    form = StudentProfileForm(instance=student_data)

    context ={
        "form" : form,
        "student_data" : student_data,
    }
    
    return render(request, "./authentication/student-profile-settings.html", context)
    
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
                messages.success(request, "Your profile has been succesfully updated")
                return redirect("studentProfileSetting")
    except Exception as e:
        handler = logging.FileHandler("./log/student_profile.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(str(e))
        messages.error(request, str(e))
        return redirect("studentProfileSetting")

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def change_password_student(request):
    form = PasswordChangeForm(user=request.user)
    
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        try:   
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully upadted!")
                return redirect("studentLogin")
        except Exception as e:
            handler = logging.FileHandler("./log/password_change.log")
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.error(str(e))
            messages.error(request, str(e))
            return redirect("changePasswordStudent")
            
    return render(request, "./authentication/change-password-student.html", {'form':form})
  
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def educationLevel(request, id):
    try:
        student_data = StudentInfo.objects.get(user_id = id)
        form = StudentInfoForm(instance=student_data)
    except StudentInfo.DoesNotExist:
        form = StudentInfoForm()
    context = {
        'form' : form
    }

    return render(request, "./authentication/update-student-edu.html", context)

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def updateEducationLevel(request, id):
    try:
        student_data = StudentInfo.objects.get(user_id = id)
        if request.method == "POST":
            form = StudentInfoForm(request.POST, instance=student_data)
            if form.is_valid():
                form.save()
                messages.success(request, "Your education label has been succesfully updated!")
                return redirect("studentProfile")
    except StudentInfo.DoesNotExist:
        if request.method == "POST":
            form = StudentInfoForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.save()
                messages.success(request, "Your education label has been succesfully updated!")
                return redirect("studentProfile")

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
                        messages.error(request, "Username already exists!!")
                        return redirect("collegeRegister")
                
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "Email already exists!!")
                        return redirect("collegeRegister")
                
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, "Your account has been successfully created!!")
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
                    logger.info(str(e))
                    messages.error(request, str(e))
                    return redirect("home")
                    
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
                messages.error(request, "Username or password dosen't match!")
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
def collegeProfileSetting(request):
    id = request.user.id
    college_data = CollegeProfile.objects.get(college_id=id)
    form = CollegeProfileForm(instance=college_data)

    context ={
        "form" : form,
        "college_data" : college_data,
    }
    
    return render(request, "./authentication/college-profile-settings.html", context)
    
#Update student profile and save it to database
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def updateCollegeProfile(request, id):
    college_data = CollegeProfile.objects.get(college_id=id)
    try:
        if request.method == "POST":
            form = CollegeProfileForm(request.POST, request.FILES, instance=college_data)
            # Update the student profile if data is valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your information has been successfully updated")
                return redirect("home")
    except ValueError as e:
        handler = logging.FileHandler("./log/college_profile.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(str(e))
        messages.error(request, str(e))
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
                messages.success(request, "Your password has been successfully updated.")
                return redirect("collegeLogin")
        except Exception as e:
            handler = logging.FileHandler("./log/password_change.log")
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.error(str(e))
            messages.error(request, str(e))
            return redirect("changePasswordCollege")
            
    return render(request, "./authentication/change-password-college.html", {'form':form})

#add college info
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def collegeInfo(request):
    form = CollegeInfoForm()
        
    context = {
        'form' : form
    }
    
    return render(request, "./authentication/update-college-info.html", context)

#save college info and save to database
@login_required(login_url="collegeLogin")
@allowed_users(allowed_roles=["COLLEGE"])
def updateCollegeInfo(request):
        if request.method == "POST":
            form = CollegeInfoForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.college_name = request.user
                data.save()
                messages.success(request, "Successfully added")
                return redirect("collegeProfile")

class UpdateCollege(UpdateView):
    template_name = "./authentication/edit_college_info.html"
    model = CollegeInfo
    form_class = CollegeInfoForm
    success_url = "/"
            
class DeleteCollege(DeleteView):
    template_name = "./authentication/collegeinfo_confirm_delete.html"
    model = CollegeInfo
    success_url = "/"
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
        return render(request, "./tests/general_test.html", {"questions": questions})

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def testResult(request):
    total_marks = 0
    correct_ans = 0
    incorect_ans = 25
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = int(key.split("_")[1])
                correct_answer = request.POST.get(f"correct_answer_{question_id}")
                if value == correct_answer:
                    total_marks += 4
                    correct_ans += 1
                    incorect_ans -= 1
                
        #Save the reult to database
        user_name = request.user
        TestResult.objects.create(user_name=user_name, total_marks=total_marks)
        context = {
            "total_marks" : total_marks,
            "correct_answer" : correct_ans,
            "incorrect_answer" : incorect_ans
        }
        return render(request, "./tests/general_test_result.html", context)

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
            correct_ans = 0
            incorect_ans = 25
            for kay, value in form.cleaned_data.items():
                selected_option = Options.objects.get(id=value)
                if selected_option.is_true:
                    total_marks += 4
                    correct_ans += 1
                    incorect_ans -= 1
        #Save the reult to database
        user_name = request.user
        TestResult.objects.create(user_name=user_name, total_marks=total_marks)
        context = {
            "total_marks" : total_marks,
            "correct_answer" : correct_ans,
            "incorrect_answer" : incorect_ans
        }
        return render(request, "./tests/verbal_test_result.html", context)             
 
# -------------------------------------- Application Form --------------------------------------
@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def application(request, id):
    form = ApplicationForm()
    college_id = id
    context = {
        "form": form,
        "college_id" : college_id
    }
    return render(request, "./authentication/application_form.html", context)

@login_required(login_url="studentLogin")
@allowed_users(allowed_roles=["STUDENT"])
def submitApplication(request):
    college_id = request.GET.get("college_id")
    test_score = TestResult.objects.filter(user_name_id = request.user.id).order_by('-date')[0]
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.first_name = request.user.first_name
            application.last_name = request.user.last_name
            application.test_score = test_score.total_marks
            application.college_name = college_id
            application.save()
            messages.success(request, "Your application has been successfully submitted.")
            return redirect("home")
        
def viewCollegeProfile(request, id):
    data = CollegeProfile.objects.get(id_user=id)
    course = CollegeInfo.objects.filter(college_name_id = id)
    
    context = {
        "data" : data,
        "course" : course
    }
    return render(request,"main/view_college_profile.html", context)