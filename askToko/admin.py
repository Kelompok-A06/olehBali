from django.contrib import admin
from .models import Question, Answer

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display=['author', 'question']
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display=['comment', 'author', 'answer']
admin.site.register(Answer, AnswerAdmin)

# sesuaikan kalau ada perubahan di modelsnya ya