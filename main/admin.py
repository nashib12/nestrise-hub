from django.contrib import admin

from .models import StudentProfile, QuestionCategory, Question, Options
# Register your models here.

admin.site.register([StudentProfile, QuestionCategory, Question, Options])
