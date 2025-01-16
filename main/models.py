import phonenumbers

from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
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
