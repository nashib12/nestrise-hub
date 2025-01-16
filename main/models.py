import phonenumbers

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Create your models here.

# Get the user id of currently logged in user
User = get_user_model()
gender_field = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other")
)
    
class StudentProfile(models.Model):
    # create student profile models here
    
    # make a connection with the objects of currently logged in user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to="student profile img", default="../static/images/profile-white.jpg")
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=100, null=True, choices=gender_field)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=200, null=True)
    
    class Meta:
        db_table = 'Student Profile'
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    # get the username from the currently logged in userid
    def __str__(self):
        return self.user.username
    
    def clean_phone_number(self):
        # Validate phone number for the Nepal region
        if self.phone_number:
            try:
                parsed_number = phonenumbers.parse(self.phone_number, "NP") 
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError({"phone_number": "Enter a valid phone number for Nepal."})
            except phonenumbers.NumberParseException:
                raise ValidationError({"phone_number": "Enter a valid phone number format."})

    def save(self, *args, **kwargs):
        self.clean_phone_number()
        super().save()

class CollegeProfile(models.Model):
    # Create college profile model here
    
    # make connection with the currently logged in user
    college = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    college_profile_img = models.ImageField(upload_to="college profile img", default="../static/images/profile-white.jpg")
    phone_number = models.CharField(null=True, max_length=15)
    address = models.CharField(max_length=100, null=True)
    websites = models.URLField(null=True, max_length=200)
    
    class Meta:
        db_table = 'College Profile'
        managed = True
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
    
    # get the username from the currently logged in userid
    def __str__(self):
        return self.college.username
    
    
    def clean_phone_number(self):
        # Validate phone number for the Nepal region
        if self.phone_number:
            try:
                parsed_number = phonenumbers.parse(self.phone_number, "NP") 
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError({"phone_number": "Enter a valid phone number for Nepal."})
            except phonenumbers.NumberParseException:
                raise ValidationError({"phone_number": "Enter a valid phone number format."})

    def save(self, *args, **kwargs):
        self.clean_phone_number()
        super().save()