from django.contrib import admin

from .models import StudentProfile, QuestionCategory, Question, Options, CollegeLocation, Gallery, Faqs, CollegeProfile
# Register your models here.

admin.site.register([StudentProfile, QuestionCategory, Question, Options, CollegeLocation, Gallery, Faqs, CollegeProfile])
