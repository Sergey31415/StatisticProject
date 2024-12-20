from django.contrib import admin

from main.models import Question, Answer, Prepod, QuestionCategory

admin.site.register(Prepod)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionCategory)