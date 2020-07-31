from django.contrib import admin
from sensei_app.models import *
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Contact)
admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Answer)


