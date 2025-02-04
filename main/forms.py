from django import forms
from django.forms import ModelForm

from .models import StudentProfile, CollegeProfile, StudentInfo, CollegeInfo, Question

# Create forms here

class StudentRegistrationForm(forms.Form):
    #Create student registration form field
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control reg-input' , 'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control reg-input' , 'placeholder':'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control reg-input' , 'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control reg-input' , 'placeholder':'Email'}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'class':'form-control reg-input' , 'placeholder':'Password','id':'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control reg-input' , 'placeholder':'Confrim Password','id':'confirmPassword'}))
    
    
class StudentProfileForm(forms.ModelForm):
    # Create student profile form field here
    class Meta:
        model = StudentProfile
        fields = ("profile_img", "date_of_birth", "gender", "phone_number", "address", "cover_image")
        widget = {
            "profile_img" : forms.FileInput(attrs={'class' : 'form-control'}),
            "date_of_birth" : forms.DateInput(attrs={'class' : 'form-control'}),
            "gender" : forms.RadioSelect(attrs={'class' : 'form-control'}),
            "phone_number" : forms.NumberInput(attrs={'class' : 'form-control', 'type':'tel', 'id':'phone'}),
            "address" : forms.TextInput(attrs={'class' : 'form-control'}),
            "cover_image" : forms.FileInput(attrs={'class':'form-control'})
        }
    
class StudentLoginForm(forms.Form):
    # Create student login form here
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control' ,'id':'password'}))
    
class CollegeProfileForm(forms.ModelForm):
    # Create college profile form here
    class Meta:
        model = CollegeProfile
        fields = ("college_name","established_date", "college_profile_img" , "phone_number", "address", "college_location", "websites", "type", "college_cover" ,"about")
        widget = {
            "college_name": forms.TextInput(attrs={'class':'form-control'}),
            "established_date": forms.DateInput(attrs={'class':'form-control'}),
            "college_profile_img" : forms.FileInput(attrs={'class':'form-control'}) , 
            "phone_number" : forms.NumberInput(attrs={'class':'form-control'}), 
            "address" : forms.TextInput(attrs={'class':'form-control'}),
            "college_location":forms.ChoiceField(), 
            "websites" : forms.TextInput(attrs={'class':'form-control'}),
            "type" : forms.RadioSelect(attrs={'class': 'form_control'}),
            "college_cover" : forms.FileInput(attrs={'class':'form-control'}),
            "about" : forms.Textarea(attrs={'class':'form-control'})
            }        

class CollegeRegistrationForm(forms.Form):
    #Create college registration form field
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control reg-input' , 'placeholder':'User Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control reg-input' , 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control reg-input' , 'placeholder':'Password','id':'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control reg-input' , 'placeholder':'Confirm Password','id':'confirmPassword'}))

class CollegeLoginForm(forms.Form):
    # Create student login form here
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password'}))
    
class StudentInfoForm(forms.ModelForm):
    #Crate student info form here
    class Meta:
        model = StudentInfo
        fields = ("education_level", "passed_year", "gpa", "grade")
        widget = {
            "education_level": forms.RadioSelect(attrs={'class':'form-control'}),
            "passed_year": forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            "gpa": forms.TextInput(attrs={'class':'form-control'}),
            "grade": forms.RadioSelect(attrs={'class':'from-control'})
        }
        
class CollegeInfoForm(forms.ModelForm):
    #Create college info from here
    class Meta:
        model = CollegeInfo
        fields = ("courses", "fee_structure", "requirements_for_enroll", "course_duration")
        widget = {
            "courses": forms.TextInput(attrs={'class':'form-control'}),
            "fee_structure": forms.NumberInput(attrs={'class':'form-control'}),
            "requriements_for_enroll": forms.TextInput(attrs={'class':'form-control'}),
            "course_duration": forms.TextInput(attrs={'class':'form-control'})
        } 

class VerbalTestForm(forms.Form):
    def __init__(self, question_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Retrieve all questions using the provided IDs
        questions = Question.objects.filter(id__in=question_ids)
        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.questions,
                choices=[(option.id, option.text) for option in question.options.all()],
                widget=forms.RadioSelect,
                required=True
            )
            
