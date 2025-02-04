from django.contrib import admin

from .models import StudentProfile, QuestionCategory, Question, Options, CollegeLocation
# Register your models here.

admin.site.register([StudentProfile, QuestionCategory, Question, Options, CollegeLocation])
