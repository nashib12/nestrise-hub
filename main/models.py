from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

# Get the user id of currently logged in user
User = get_user_model()


class StudentProfile(models.Model):
    # create student profile models here
    
    # make a connection with the objects of currently logged in user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to="student profile img", default="../static/images/profile-white.jpg")
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=100, null=True)
    phone_number = PhoneNumberField(null=True)
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
        data = self.cleaned_data['phone_number']
        # Remove any non-numeric characters
        cleaned_number = ''.join(filter(str.isdigit, data))

        # Validate phone number length (e.g., 10 digits for US numbers)
        if len(cleaned_number) < 10 or len(cleaned_number) > 15:
            raise models.ValidationError("Enter a valid phone number.")
        
        return cleaned_number
