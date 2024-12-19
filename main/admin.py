from django.contrib import admin

from main.models import Questions, Answer, Prepod

admin.site.register(Prepod)
admin.site.register(Questions)
admin.site.register(Answer)