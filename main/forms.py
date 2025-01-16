from django import forms
from django.forms import ModelForm

from .models import StudentProfile, CollegeProfile

# Create forms here

class StudentRegistrationForm(forms.Form):
    #Create student registration form field
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    
class StudentProfileForm(forms.ModelForm):
    # Create student profile form field here
    class Meta:
        model = StudentProfile
        fields = ("profile_img", "date_of_birth", "gender", "phone_number", "address")
        widget = {
            "profile_img" : forms.FileInput(attrs={'class' : 'form-control'}),
            "date_of_birth" : forms.DateInput(attrs={'class' : 'form-control'}),
            "gender" : forms.RadioSelect(attrs={'class' : 'form-control'}),
            "phone_number" : forms.NumberInput(attrs={'class' : 'form-control', 'type':'tel', 'id':'phone'}),
            "address" : forms.TextInput(attrs={'class' : 'form-control'}),
        }
    
class StudentLoginForm(forms.Form):
    # Create student login form here
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class CollegeProfileForm(forms.ModelForm):
    # Create college profile form here
    class Meta:
        model = CollegeProfile
        fields = ("college_profile_img" , "phone_number", "address", "websites")
        widget = {
            "college_profile_img" : forms.FileInput(attrs={'class':'form-control'}) , 
            "phone_number" : forms.NumberInput(attrs={'class':'from-control'}), 
            "address" : forms.TextInput(attrs={'class':'form-control'}), 
            "websites" : forms.TextInput(attrs={'class':'form-control'})
            }        

class CollegeRegistrationForm(forms.Form):
    #Create college registration form field
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class CollegeLoginForm(forms.Form):
    # Create student login form here
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    