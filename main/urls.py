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
    
        
    # ----------------------------- authentication -----------------------------
    path("selection/",selection,name="selection"),
    # ----------- student authentication section ----------- 
    path("registration/", studentRegister, name="studentRegister"),
    path("studentlogin/",studentLogin,name="studentLogin"),
    path("studentlogout/",studentLogout,name="studentLogout"),
    path("studentprofilesettings/<int:id>",studentProfileSetting,name="studentProfileSetting"),
    path("studentprofileupdate/<int:id>/",updateStudentProfile,name="studentProfileUpdate"),
    path("change_password_college/", change_password_student, name="changePasswordStudent"),
    
    # ----------- college authentication section ----------- 
    path("collegeregistration/", collegeRegister, name="collegeRegister"),
    path("collegelogin/",collegeLogin,name="collegeLogin"),
    path("collegelogout/",collegeLogout,name="collegeLogout"),
    path("collegeprofilesettings/<int:id>",collegeProfileSetting,name="collegeProfileSetting"),
    path("collegeprofileupdate/<int:id>/",updateCollegeProfile,name="collegeProfileUpdate"),
    path("changepasswordcollege/", change_password_college, name="changePasswordCollege"),

    
    # ---------------- password reset section ----------------
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name=""), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name=""), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name=""), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name=""), name='password_reset_complete'), 
]
