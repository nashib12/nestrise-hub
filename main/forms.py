from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import PasswordChangeForm

from .models import StudentProfile, CollegeProfile, StudentInfo, CollegeInfo, Question, Application

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
        widgets = {
            "profile_img" : forms.FileInput(attrs={'class': 'form-control fs-5' ,'id' : 'image', 'type' : 'file'}),
            "date_of_birth" : forms.DateInput(attrs={'class': 'form-control fs-5', 'id' : 'dob' ,'type' : 'date'}),
            "gender" : forms.Select(attrs={'class': 'form-control fs-5', 'id' : 'gender'}),
            "phone_number" : forms.TextInput(attrs={'class': 'form-control fs-5', 'type':'tel', 'id':'phone'}),
            "address" : forms.TextInput(attrs={'class': 'form-control fs-5', 'id' : 'address'}),
            "cover_image" : forms.FileInput(attrs={'class':'form-control fs-5', 'id' : 'cover_img', 'type' : 'file'})
        }
        
        labels = {
            "profile_img" : "", 
            "date_of_birth" : "", 
            "gender" : "", 
            "phone_number" : "", 
            "address" : "", 
            "cover_image" : ""
        }
        
class StudentLoginForm(forms.Form):
    # Create student login form here
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control' ,'id':'password'}))
    
class CollegeProfileForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget())
    # Create college profile form here
    class Meta:
        model = CollegeProfile
        fields = ("college_name","established_date", "college_profile_img" , "phone_number", "address", "college_location", "websites", "type", "college_cover" ,"about")
        widgets = {
            "college_name": forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'c_name'}),
            "established_date": forms.DateInput(attrs={'class':'form-control fs-5', 'id' : 'date', 'type' : 'date'}),
            "college_profile_img" : forms.FileInput(attrs={'class':'form-control fs-5', 'id' : 'profile'}) , 
            "phone_number" : forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'phone'}), 
            "address" : forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'address'}),
            "college_location":forms.Select(attrs={'class' : 'form-control fs-5', 'id' : 'location'}), 
            "websites" : forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'website'}),
            "type" : forms.Select(attrs={'class': 'form-control fs-5', 'id' : 'type'}),
            "college_cover" : forms.FileInput(attrs={'class':'form-control fs-5', 'id' : 'cover'}),
            "about" : CKEditorWidget(),
            }     
        
        labels = {
            "college_name" : "",
            "established_date" : "", 
            "college_profile_img" : "" , 
            "phone_number" : "", 
            "address" : "", 
            "college_location" : "", 
            "websites" : "", 
            "type" : "", 
            "college_cover" : "" ,
            "about" : "",
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
        labels = {
            'education_level' : '',
            'passed_year' : '',
            'gpa' : '',
            'grade' : '',
        }
        widgets = {
            "education_level": forms.Select(attrs={'class':'form-control fs-5', 'id' : 'level'}),
            "passed_year": forms.DateInput(attrs={'class':'form-control fs-5', 'id' : 'year', 'type':'date'}),
            "gpa": forms.TextInput(attrs={'class':'form-control fs-5' , 'id' : 'gpa'}),
            "grade": forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'grade'}),
        }
        
class CollegeInfoForm(forms.ModelForm):
    #Create college info from here
    class Meta:
        model = CollegeInfo
        fields = ("courses", "fee_structure", "requirements_for_enroll", "course_duration")
        widgets = {
            "courses": forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'course'}),
            "fee_structure": forms.NumberInput(attrs={'class':'form-control fs-5', 'id' : 'fee'}),
            "requirements_for_enroll": forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'requirements'}),
            "course_duration": forms.TextInput(attrs={'class':'form-control fs-5', 'id' : 'duration'})
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
                widgets=forms.RadioSelect,
                required=True
            )
            
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = {'contact', 'course'}
        labels = {
            'contact' : '',
            'course' : '',
        }
        
        widgetss = {
           'contact' : forms.TextInput(attrs={'class' : 'form-control fs-5', 'id' : 'contact'}),
           'course' : forms.Select(attrs={'class' : 'form-control fs-5', 'id' : 'course'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].empty_label = "Select a course"
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['old_password'].label = ''
        self.fields['old_password'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['old_password'].widget.attrs['id'] = 'old_password'
        
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['new_password1'].widget.attrs['id'] = 'password1'
        
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['new_password2'].widget.attrs['id'] = 'password2'