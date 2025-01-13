from django import forms

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
    
    
class StudentProfileForm(forms.Form):
    # Create student profile form filed here
    profile_img = forms.ImageField(label="Profile Images", widget=forms.FileInput(attrs={'class':'form-control'}))
    date_of_birth = forms.DateField(label="Dte of Birth", widget=forms.DateInput)
    gender = forms.ChoiceField(label = "Gender", choices=gender, widget=forms.RadioSelect)
    phone_number = forms.IntegerField(label="Phone Number", widget=forms.NumberInput(attrs={'class': 'from-control', 'id':'phone', 'type':'tel'}))
    address = forms.CharField()

    
    