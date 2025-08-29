from django.contrib import admin
from .models import Quiz, Question,  QuizAttempt, Answer



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "created_by")
    inlines = [QuestionInline]
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz")
    


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "started_at","completed_at")
    inlines = [AnswerInline]
    readonly_fields = ("score",  "started_at", "completed_at")


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(Answer)
