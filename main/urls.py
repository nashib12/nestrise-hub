"""
URL configuration for nestApp app.

The `urlpatterns` list routes URLs to views.

import function or class base views from views.py files

"""
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

#create urlpatterns here

urlpatterns = [
    path("",home,name="home"), 
    path("collegeAbroad/", collegeAbroad, name="collegeAbroad"),
    path("collegeNepal/", collegeNepal, name="collegeNepal"),
    path("studentProfile/<int:id>", studentProfile, name="studentProfile"),
    path("collegeProfile/<int:id>", collegeProfile, name="collegeProfile"),
    # ----------------------------- authentication -----------------------------
    path("selection/",selection,name="selection"),
    # ----------- student authentication section ----------- 
    path("registration/", studentRegister, name="studentRegister"),
    path("studentlogin/",studentLogin,name="studentLogin"),
    path("studentlogout/",studentLogout,name="studentLogout"),
    path("studentprofilesettings/",studentProfileSetting,name="studentProfileSetting"),
    path("studentprofileupdate/<int:id>/",updateStudentProfile,name="studentProfileUpdate"),
    path("change_password_college/", change_password_student, name="changePasswordStudent"),
    path("eductaionLevel/<int:id>", educationLevel, name="educationLevel"),
    path("updateEducationLevel/<int:id>/", updateEducationLevel, name="updateEducationLevel"),
    
    # ----------- college authentication section ----------- 
    path("collegeregistration/", collegeRegister, name="collegeRegister"),
    path("collegelogin/",collegeLogin,name="collegeLogin"),
    path("collegelogout/",collegeLogout,name="collegeLogout"),
    path("collegeprofilesettings/",collegeProfileSetting,name="collegeProfileSetting"),
    path("collegeprofileupdate/<int:id>/",updateCollegeProfile,name="collegeProfileUpdate"),
    path("changepasswordcollege/", change_password_college, name="changePasswordCollege"),
    path("collegeInfo/", collegeInfo, name="collegeInfo"),
    path("updateCollegeInfo/", updateCollegeInfo, name="updateCollegeInfo"),
    path("editCollegeInfo/<int:pk>", UpdateCollege.as_view(), name="editCollegeInfo"),
    path("deleteCollegeInfo/<int:pk>", DeleteCollege.as_view(), name="deleteCollegeInfo"),

    # ---------------- password reset section ----------------
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="./password_reset/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="./password_reset/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="./password_reset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="./password_reset/password_reset_complete.html"), name='password_reset_complete'),
    
    # -------------------------------- Apptitiude test section --------------------------------
    path('test/',categorySelection, name="testCategory"),
    path('generaltest/', aptitudeTest, name="test"),
    path('generaltestresult/', testResult, name="result"),
    path('verbaltest/',verbalReasoningTest, name="verbalTest"),
    path('verbaltestresult/',verbalTestCheck, name="verbalTestResult"),
    
     # -------------------------------- Application section --------------------------------
     path('applicationForm/<int:id>', application, name="application"),
     path('submitApplication/', submitApplication, name="submitApplication"),
     path("viewCollegeProfile/<int:id>", viewCollegeProfile, name="viewCollegeProfile"),
]
