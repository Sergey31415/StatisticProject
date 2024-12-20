from django.contrib import admin

from main.models import QuestionnaireItem, Answer, Prepod

admin.site.register(Prepod)
admin.site.register(QuestionnaireItem)
admin.site.register(Answer)