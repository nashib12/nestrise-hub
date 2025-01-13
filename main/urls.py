"""
URL configuration for nestApp app.

The `urlpatterns` list routes URLs to views.

import function or class base views from views.py files

"""
from django.urls import path

from .views import *

#create urlpatterns here

urlpatterns = [
    path("",home,name="home"), 
    
        
    # ----------------------------- authentication -----------------------------
    
    path("registration/", student_register, name="student-register"),
]
