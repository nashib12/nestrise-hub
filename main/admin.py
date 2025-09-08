from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register([StudentProfile, QuestionCategory, Question, Options, CollegeLocation, Gallery, Faqs, CollegeProfile, NewsCategory, EventCategory])

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('tes_name', 'tes_message', 'created_at')
    
@admin.register(New)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'author', 'date')
    list_filter = ('category',)
    ordering = ['-date']
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'organizer', 'location', 'event_date')
    list_filter = ('category', 'location')
    ordering = ['-event_date']
    