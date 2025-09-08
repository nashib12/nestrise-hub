import phonenumbers

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

# Create your models here.

# Get the user id of currently logged in user
User = get_user_model()
gender_field = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other")
)

education_field = (
    ("S.L.C./S.E.E.", "S.L.C./S.E.E."),
    ("+2", "+2"),
    ("Bachelor Degree", "Bachelor Degree"),
    ("Masters", "Masters")
)

grade_field = (
    ("Percntage", "Percentage"),
    ("G.P.A.", "G.P.A.")
)

college_type = (
    ("Private", "Private"),
    ("Government", "Govenment")
)

class StudentProfile(models.Model):
    # create student profile models here
    
    # make a connection with the objects of currently logged in user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to="student profile img", default="../static/images/profile-white.jpg")
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=100, null=True, choices=gender_field)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=200, null=True)
    cover_image = models.ImageField(upload_to="student cover img", blank=True)
    
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

class CollegeLocation(models.Model):
    location = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'College Location'
        managed = True
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        
    def __str__(self):
        return self.location
    
class CollegeProfile(models.Model):
    # Create college profile model here
    # make connection with the currently logged in user
    college = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    college_name = models.CharField(max_length=200, blank=True)
    college_profile_img = models.ImageField(upload_to="college profile img", default="../static/images/profile-white.jpg")
    established_date = models.DateField(null=True)
    phone_number = models.CharField(null=True, max_length=15)
    address = models.CharField(max_length=100, null=True)
    college_location = models.ForeignKey(CollegeLocation, on_delete=models.CASCADE, blank=True, null=True)
    websites = models.URLField(null=True, max_length=200)
    type = models.CharField(null=True, choices=college_type, max_length=20)
    college_cover = models.ImageField(upload_to="college profle cover", default="../static/images/profile-white.jpg")
    about = RichTextField(default="")
    
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
        
class StudentInfo(models.Model):
    #Create models field for additional student information
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=30, choices=education_field, null=True)
    passed_year = models.DateField(null=True)
    gpa = models.CharField(max_length=10, choices=grade_field, null=True)
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    
    class Meta:
        db_table = 'Student Info'
        managed = True
        verbose_name = 'StudentInfo'
        verbose_name_plural = 'StudentInfos'
        
    def __str__(self):
        return self.user.username

class CollegeInfo(models.Model):
    # Create model fields for additional college information
    college_name = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.CharField(max_length=100)
    fee_structure = models.DecimalField(max_digits=9, decimal_places=2)
    requirements_for_enroll = models.CharField(max_length=200)
    course_duration = models.CharField(max_length=20, null=True)
    
    class Meta:
        db_table = 'College Info'
        managed = True
        verbose_name = 'CollegeInfo'
        verbose_name_plural = 'CollegeInfos'
        
    def __str__(self):
        return self.courses

class TestResult(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True) 

    class Meta:
        db_table = 'Test Result'
        managed = True
        verbose_name = 'Totalmark'
        verbose_name_plural = 'Totalmarks'
    
    def __str__(self):
        return f"{self.user_name} - {self.total_marks}"
    
class QuestionCategory(models.Model):
    category = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'Question Category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.category
    
class Question(models.Model):
    question_category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    questions = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'Question'
        managed = True
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        
    def __str__(self):
        return self.questions
    
class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)
    is_true = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Answer Option'
        managed = True
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        
    def __str__(self):
        return self.text
    
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    course = models.ForeignKey(CollegeInfo, on_delete=models.CASCADE)
    test_score = models.CharField(max_length=100)
    application_status = models.CharField(max_length=50, default= "Pending")
    submitted_date = models.DateField(auto_now_add=True)
    college_name = models.IntegerField()
    
    class Meta:
        db_table = 'Application List'
        managed = True
        verbose_name = 'Application'
        verbose_name_plural = 'Applications' 
    
        
    def clean_phone_number(self):
        # Validate phone number for the Nepal region
        if self.contact:
            try:
                parsed_number = phonenumbers.parse(self.contact, "NP") 
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError({"phone_number": "Enter a valid phone number for Nepal."})
            except phonenumbers.NumberParseException:
                raise ValidationError({"phone_number": "Enter a valid phone number format."})

    def save(self, *args, **kwargs):
        self.clean_phone_number()
        super().save()
        
class Gallery(models.Model):
    image = models.ImageField(upload_to="gallery img")
    image_title = models.CharField(max_length=100)
    image_desc = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'Gallery'
        managed = True
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        
class Faqs(models.Model):
    faq_question = models.CharField(max_length=100)
    faq_answer = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'FAQs'
        managed = True
        verbose_name = 'Faq'
        verbose_name_plural = 'Faqs'
        
class Testimonial(models.Model):
    tes_img = models.ImageField(upload_to="testimonial/")
    tes_name = models.CharField(max_length=100)
    tes_message = models.TextField()
    tes_title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Testimonials'
        managed = True
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-created_at']
        
class NewsCategory(models.Model):
    category = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'News Category'
        managed = True
    
    def __str__(self):
        return self.category
    
class EventCategory(models.Model):
    category = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'Events Category'
        managed = True
    
    def __str__(self):
        return self.category
    
class New(models.Model):
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name="news")
    news_title = models.CharField(max_length=50)
    news_description = RichTextField()
    author = models.CharField(max_length=50)
    author_img = models.ImageField(upload_to="news/author/", blank=True, null=True)
    news_img = models.ImageField(upload_to="news/images/")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    class Mets:
        db_table = "News"
        managed = True
        ordering = ['-created_at']
    
    def __str__(self):
        return self.news_title
    
class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name="events")
    event_title = models.CharField(max_length=50)
    event_description = RichTextField()
    organizer = models.CharField(max_length=50)
    poster = models.ImageField(upload_to="events/")
    location = models.CharField(max_length=150)
    event_date = models.DateField()
    event_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        db_table = "Events"
        managed = True
    
    def __str__(self):
        return self.event_title    