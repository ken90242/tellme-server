from django.contrib import admin

from .models import News

# Register your models here.
# class NewsAdmin(admin.ModelAdmin):
#     # fields = ['pub_date', 'question_text']
#     list_display  = [f.name for f in News._meta.fields]

admin.site.register(News)
# Register your models here.
