from django import forms
from django.forms import ModelForm

from .models import StudentProfile

# Create forms here

# Choices for gender field
gender = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other")
)

class StudentRegistrationForm(forms.Form):
    #Create student registration form field
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    
class StudentProfileForm(forms.ModelForm):
    # Create student profile form filed here
    class Meta:
        model = StudentProfile
        fields = ("profile_img", "date_of_birth", "gender", "phone_number", "address")
        widget = {
            "profile_img" : forms.FileInput(attrs={'class' : 'form-control'}),
            "date_of_birth" : forms.DateInput(attrs={'class' : 'form-control'}),
            "gender" : forms.TextInput(attrs={'class' : 'form-control'}),
            "phone_number" : forms.NumberInput(attrs={'class' : 'form-control'}),
            "address" : forms.TextInput(attrs={'class' : 'form-control'}),
        }

    
    
class StudentLoginForm(forms.Form):
    # Create student login form here
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    
    