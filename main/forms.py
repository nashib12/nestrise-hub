from django import forms
from django.forms import ModelForm

from .models import StudentProfile, CollegeProfile, StudentInfo, CollegeInfo, Question, Options

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
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class CollegeProfileForm(forms.ModelForm):
    # Create college profile form here
    class Meta:
        model = CollegeProfile
        fields = ("established_date", "college_profile_img" , "phone_number", "address", "websites", "type", "college_cover" ,"about")
        widget = {
            "established_date": forms.DateInput(attrs={'class':'from-control'}),
            "college_profile_img" : forms.FileInput(attrs={'class':'form-control'}) , 
            "phone_number" : forms.NumberInput(attrs={'class':'from-control'}), 
            "address" : forms.TextInput(attrs={'class':'form-control'}), 
            "websites" : forms.TextInput(attrs={'class':'form-control'}),
            "type" : forms.RadioSelect(attrs={'class': 'form_control'}),
            "college_cover" : forms.FileInput(attrs={'class':'from-control'}),
            "about" : forms.Textarea(attrs={'class':'from-control'})
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
