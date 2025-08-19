from django.contrib import admin
from .models import Question, Option, ExamAttempt

class OptionInline(admin.TabularInline):
    model = Option
    extra = 0

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ("id", "text")

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'started_at', 'submitted_at')

admin.site.register(Option)
